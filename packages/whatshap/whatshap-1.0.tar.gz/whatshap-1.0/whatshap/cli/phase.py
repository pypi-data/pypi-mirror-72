#!/usr/bin/env python3
"""
Phase variants in a VCF with the WhatsHap algorithm

Read a VCF and one or more files with phase information (BAM/CRAM or VCF phased
blocks) and phase the variants. The phased VCF is written to standard output.
"""
import logging
import sys
import platform

from argparse import SUPPRESS
from collections import defaultdict
from copy import deepcopy

from contextlib import ExitStack
from whatshap.vcf import VcfReader, PhasedVcfWriter, GenotypeLikelihoods, VcfError
from whatshap import __version__
from whatshap.core import (
    ReadSet,
    readselection,
    Pedigree,
    PedigreeDPTable,
    NumericSampleIds,
    PhredGenotypeLikelihoods,
    compute_genotypes,
    HapChatCore,
)
from whatshap.graph import ComponentFinder
from whatshap.pedigree import (
    PedReader,
    mendelian_conflict,
    UniformRecombinationCostComputer,
    GeneticMapRecombinationCostComputer,
    find_recombination,
    ParseError,
)
from whatshap.timer import StageTimer
from whatshap.utils import plural_s
from whatshap.cli import CommandLineError, log_memory_usage, PhasedInputReader
from whatshap.merge import ReadMerger, DoNothingReadMerger

__author__ = "Murray Patterson, Alexander Schönhuth, Tobias Marschall, Marcel Martin"

logger = logging.getLogger(__name__)


def find_components(phased_positions, reads, master_block=None, heterozygous_positions=None):
    """
    Return a dict that maps each variant position to the component it is in.
    Variants are considered to be in the same component if a read exists that
    covers both. A component is identified by the position of its leftmost
    variant.
    master_block -- List of positions in a "master block", i.e. all blocks containing
                    any of these positions are merged into one block.
    heterozygous_positions -- A dictionary mapping numeric sample ids to sets of
                              positions. Component building is then restricted to variants
                              at these positions. If none, all variants are used.
    """
    logger.debug("Finding connected components ...")
    assert phased_positions == sorted(phased_positions)

    # Find connected components.
    # A component is identified by the position of its leftmost variant.
    component_finder = ComponentFinder(phased_positions)
    phased_positions = set(phased_positions)
    for read in reads:
        if heterozygous_positions is None:
            positions = [
                variant.position for variant in read if variant.position in phased_positions
            ]
        else:
            positions = [
                variant.position
                for variant in read
                if (variant.position in phased_positions)
                and (variant.position in heterozygous_positions[read.sample_id])
            ]
        for position in positions[1:]:
            component_finder.merge(positions[0], position)
    if master_block is not None:
        for position in master_block[1:]:
            component_finder.merge(master_block[0], position)
    components = {position: component_finder.find(position) for position in phased_positions}
    return components


def find_largest_component(components):
    """
    Determine the largest component and return a sorted list of positions
    contained in it.
    components -- dictionary mapping positin to block_id as returned by find_components.
    """
    blocks = defaultdict(list)
    for position, block_id in components.items():
        blocks[block_id].append(position)
    largest = []
    for block in blocks.values():
        if len(block) > len(largest):
            largest = block
    largest.sort()
    return largest


def best_case_blocks(reads):
    """
    Given a list of core reads, determine the number of phased blocks that
    would result if each variant were actually phased.

    Return the number of connected components and non-singleton components.
    """
    positions = set()
    for read in reads:
        for variant in read:
            positions.add(variant.position)
    component_finder = ComponentFinder(positions)
    for read in reads:
        read_positions = [variant.position for variant in read]
        for position in read_positions[1:]:
            component_finder.merge(read_positions[0], position)
    # A dict that maps each component to the number of variants it contains
    component_sizes = defaultdict(int)
    for position in positions:
        component_sizes[component_finder.find(position)] += 1
    non_singletons = [component for component, size in component_sizes.items() if size > 1]
    return len(component_sizes), len(non_singletons)


def select_reads(readset, max_coverage, preferred_source_ids):
    logger.info(
        "Reducing coverage to at most %dX by selecting most informative reads ...", max_coverage,
    )
    selected_indices = readselection(readset, max_coverage, preferred_source_ids)
    selected_reads = readset.subset(selected_indices)
    logger.info(
        "Selected %d reads covering %d variants",
        len(selected_reads),
        len(selected_reads.get_positions()),
    )

    return selected_reads


class ReadList:
    """Write a list of reads that has been used for phasing to a file"""

    def __init__(self, path):
        self._path = path
        self._file = None

    def __enter__(self):
        self._file = open(self._path, "w")
        print(
            "#readname",
            "source_id",
            "sample",
            "phaseset",
            "haplotype",
            "covered_variants",
            "first_variant_pos",
            "last_variant_pos",
            sep="\t",
            file=self._file,
        )
        return self

    def __exit__(self, *args):
        self._file.close()
        self._file = None

    def write(self, readset, bipartition, sample_components, numeric_sample_ids):
        """
        readset -- core.ReadSet object with reads to be written
        bipartition -- bipartition of reads, i.e. iterable with one entry from {0,1} for each read in readset
        sample_components -- a dictionary that maps each sample to its connected components

                Each component in turn is a dict that maps each variant position to a
                component, where a component is identified by the position of its
                left-most variant

        numeric_sample_ids -- core.NumericSampleIds object mapping sample names to numeric ids as stored in each read
        """
        if self._file is None:
            raise ValueError("Needs to be used as context manager (e.g. in a with statement")
        assert len(readset) == len(bipartition)
        numeric_id_to_name = numeric_sample_ids.inverse_mapping()
        for read, haplotype in zip(readset, bipartition):
            sample = numeric_id_to_name[read.sample_id]
            components = sample_components[sample]
            phaseset = components[read[0].position] + 1
            print(
                read.name,
                read.source_id,
                sample,
                phaseset,
                haplotype,
                len(read),
                read[0].position + 1,
                read[-1].position + 1,
                file=self._file,
            )


def setup_pedigree(ped_path, numeric_sample_ids, samples):
    """
    Read in PED file to set up list of relationships.

    Return a pair (trios, pedigree_samples), where trios is a list of Trio
    objects and pedigree_samples is the set of all samples that are mentioned
    in the PED file (as individual, mother or father).

    ped_path -- path to PED file
    samples -- samples to be phased
    """
    trios = []
    pedigree_samples = set()
    for trio in PedReader(ped_path):
        if trio.child is None or trio.mother is None or trio.father is None:
            logger.warning(
                "Relationship %s/%s/%s ignored "
                "because at least one of the individuals is unknown",
                trio.child,
                trio.mother,
                trio.father,
            )
            continue
        # if at least one individual is not in samples, skip trio
        if (
            (trio.mother not in samples)
            or (trio.father not in samples)
            or (trio.child not in samples)
        ):
            # happens in case --ped and --samples are used
            logger.warning(
                "Relationship %s/%s/%s ignored because at least one of the "
                "individuals was not given by --samples.",
                trio.child,
                trio.mother,
                trio.father,
            )
            continue

        trios.append(trio)
        pedigree_samples.add(trio.child)
        pedigree_samples.add(trio.father)
        pedigree_samples.add(trio.mother)
        # Ensure that all mentioned individuals have a numeric id
        _ = numeric_sample_ids[trio.child]

    return trios, pedigree_samples


def run_whatshap(
    phase_input_files,
    variant_file,
    reference=None,
    output=sys.stdout,
    samples=None,
    chromosomes=None,
    ignore_read_groups=False,
    indels=True,
    mapping_quality=20,
    read_merging=False,
    read_merging_error_rate=0.15,
    read_merging_max_error_rate=0.25,
    read_merging_positive_threshold=1000000,
    read_merging_negative_threshold=1000,
    max_coverage=15,
    full_genotyping=False,
    distrust_genotypes=False,
    include_homozygous=False,
    ped=None,
    recombrate=1.26,
    genmap=None,
    genetic_haplotyping=True,
    recombination_list_filename=None,
    tag="PS",
    read_list_filename=None,
    gl_regularizer=None,
    gtchange_list_filename=None,
    default_gq=30,
    write_command_line_header=True,
    use_ped_samples=False,
    algorithm="whatshap",
):
    """
    Run WhatsHap.

    phase_input_files -- list of paths to BAM/CRAM/VCF files
    variant_file -- path to input VCF
    reference -- path to reference FASTA
    output -- path to output VCF or a file-like object
    samples -- names of samples to phase. an empty list means: phase all samples
    chromosomes -- names of chromosomes to phase. an empty list means: phase all chromosomes
    ignore_read_groups
    mapping_quality -- discard reads below this mapping quality
    read_merging -- whether or not to merge reads
    read_merging_error_rate -- probability that a nucleotide is wrong
    read_merging_max_error_rate -- max error rate on edge of merge graph considered
    read_merging_positive_threshold -- threshold on the ratio of the two probabilities
    read_merging_negative_threshold -- threshold on the opposite ratio of positive threshold
    max_coverage
    full_genotyping
    distrust_genotypes
    include_homozygous
    genetic_haplotyping -- in ped mode, merge disconnected blocks based on genotype status
    recombination_list_filename -- filename to write putative recombination events to
    tag -- How to store phasing info in the VCF, can be 'PS' or 'HP'
    read_list_filename -- name of file to write list of used reads to
    algorithm -- algorithm to use, can be 'whatshap' or 'hapchat'
    gl_regularizer -- float to be passed as regularization constant to GenotypeLikelihoods.as_phred
    gtchange_list_filename -- filename to write list of changed genotypes to
    default_gq -- genotype likelihood to be used when GL or PL not available
    write_command_line_header -- whether to add a ##commandline header to the output VCF
    """

    if algorithm == "hapchat" and ped is not None:
        raise CommandLineError("The hapchat algorithm cannot do pedigree phasing")

    timers = StageTimer()
    logger.info(
        "This is WhatsHap %s running under Python %s", __version__, platform.python_version(),
    )
    if full_genotyping:
        distrust_genotypes = True
        include_homozygous = True
    numeric_sample_ids = NumericSampleIds()
    if write_command_line_header:
        command_line = "(whatshap {}) {}".format(__version__, " ".join(sys.argv[1:]))
    else:
        command_line = None

    if read_merging:
        read_merger = ReadMerger(
            read_merging_error_rate,
            read_merging_max_error_rate,
            read_merging_positive_threshold,
            read_merging_negative_threshold,
        )
    else:
        read_merger = DoNothingReadMerger()

    with ExitStack() as stack:
        try:
            vcf_writer = stack.enter_context(
                PhasedVcfWriter(
                    command_line=command_line, in_path=variant_file, out_file=output, tag=tag,
                )
            )
        except (OSError, VcfError) as e:
            raise CommandLineError(e)

        phased_input_reader = stack.enter_context(
            PhasedInputReader(
                phase_input_files,
                reference,
                numeric_sample_ids,
                ignore_read_groups,
                mapq_threshold=mapping_quality,
                indels=indels,
            )
        )
        show_phase_vcfs = phased_input_reader.has_vcfs

        # Only read genotype likelihoods from VCFs when distrusting genotypes
        vcf_reader = stack.enter_context(
            VcfReader(variant_file, indels=indels, genotype_likelihoods=distrust_genotypes)
        )

        if ignore_read_groups and not samples and len(vcf_reader.samples) > 1:
            raise CommandLineError(
                "When using --ignore-read-groups on a VCF with "
                "multiple samples, --sample must also be used."
            )
        if not samples:
            samples = vcf_reader.samples

        # if --use-ped-samples is set, use only samples from PED file
        if ped and use_ped_samples:
            samples = PedReader(ped).samples()

        raise_if_any_sample_not_in_vcf(vcf_reader, samples)

        if ped and genmap:
            logger.info(
                "Using region-specific recombination rates from genetic map %s.", genmap,
            )
            try:
                recombination_cost_computer = GeneticMapRecombinationCostComputer(genmap)
            except ParseError as e:
                raise CommandLineError(e)
        else:
            if ped:
                logger.info("Using uniform recombination rate of %g cM/Mb.", recombrate)
            recombination_cost_computer = UniformRecombinationCostComputer(recombrate)

        samples = frozenset(samples)
        families, family_trios = setup_families(samples, ped, numeric_sample_ids, max_coverage)

        read_list = None
        if read_list_filename:
            read_list = stack.enter_context(ReadList(read_list_filename))
            if algorithm == "hapchat":
                logger.warning(
                    "On which haplotype a read occurs in the inferred solution is not yet "
                    "implemented in hapchat, and so the corresponding column in the "
                    "read list file contains no information about this"
                )

        with timers("parse_phasing_vcfs"):
            # TODO should this be done in PhasedInputReader.__init__?
            phased_input_reader.read_vcfs()

        for variant_table in timers.iterate("parse_vcf", vcf_reader):
            chromosome = variant_table.chromosome
            if (not chromosomes) or (chromosome in chromosomes):
                logger.info("======== Working on chromosome %r", chromosome)
            else:
                logger.info(
                    "Leaving chromosome %r unchanged (present in VCF but not requested by option --chromosome)",
                    chromosome,
                )
                with timers("write_vcf"):
                    superreads, components = dict(), dict()
                    vcf_writer.write(chromosome, superreads, components)
                continue

            if full_genotyping:
                positions = [v.position for v in variant_table.variants]
                for sample in samples:
                    logger.info("---- Initial genotyping of %s", sample)
                    with timers("read_bam"):
                        bam_sample = None if ignore_read_groups else sample
                        readset, vcf_source_ids = phased_input_reader.read(
                            chromosome, variant_table.variants, bam_sample, read_vcf=False,
                        )
                        readset.sort()  # TODO can be removed
                        genotypes, genotype_likelihoods = compute_genotypes(readset, positions)
                        variant_table.set_genotypes_of(sample, genotypes)
                        variant_table.set_genotype_likelihoods_of(
                            sample, [GenotypeLikelihoods(gl) for gl in genotype_likelihoods],
                        )

            # These two variables hold the phasing results for all samples
            superreads, components = dict(), dict()

            # Iterate over all families to process, i.e. a separate DP table is created
            # for each family.
            # TODO: Can the body of this loop be factored out into a phase_family function?
            for representative_sample, family in sorted(families.items()):
                if len(family) == 1:
                    logger.info("---- Processing individual %s", representative_sample)
                else:
                    logger.info("---- Processing family with individuals: %s", ",".join(family))
                max_coverage_per_sample = max(1, max_coverage // len(family))
                logger.info("Using maximum coverage per sample of %dX", max_coverage_per_sample)
                trios = family_trios[representative_sample]
                assert len(family) == 1 or len(trios) > 0

                homozygous_positions, phasable_variant_table = find_phaseable_variants(
                    family, include_homozygous, trios, variant_table
                )

                # Get the reads belonging to each sample
                readsets = dict()  # TODO this could become a list
                for sample in family:
                    with timers("read_bam"):
                        readset, vcf_source_ids = phased_input_reader.read(
                            chromosome, phasable_variant_table.variants, sample,
                        )

                    # TODO: Read selection done w.r.t. all variants, where using heterozygous
                    #  variants only would probably give better results.
                    with timers("select"):
                        readset = readset.subset(
                            [i for i, read in enumerate(readset) if len(read) >= 2]
                        )
                        logger.info(
                            "Kept %d reads that cover at least two variants each", len(readset),
                        )
                        merged_reads = read_merger.merge(readset)
                        selected_reads = select_reads(
                            merged_reads,
                            max_coverage_per_sample,
                            preferred_source_ids=vcf_source_ids,
                        )

                    readsets[sample] = selected_reads
                    if len(family) == 1 and not distrust_genotypes:
                        # When having a pedigree (len(family) > 1), blocks are also merged after
                        # phasing based on the pedigree information and these statistics are not
                        # so useful. When distrust_genotypes, genotypes can change during phasing
                        # and so can the block structure. So don't print these stats in those cases
                        log_best_case_phasing_info(readset, selected_reads)

                all_reads = merge_readsets(readsets)

                # Determine which variants can (in principle) be phased
                accessible_positions = sorted(all_reads.get_positions())
                logger.info(
                    "Variants covered by at least one phase-informative "
                    "read in at least one individual after read selection: %d",
                    len(accessible_positions),
                )
                if len(family) > 1 and genetic_haplotyping:
                    # In case of genetic haplotyping, also retain all positions homozygous
                    # in at least one individual (because they might be phased based on genotypes)
                    accessible_positions = sorted(
                        set(accessible_positions).union(homozygous_positions)
                    )
                    logger.info(
                        "Variants either covered by phase-informative read or homozygous "
                        "in at least one individual: %d",
                        len(accessible_positions),
                    )

                # Keep only accessible positions
                phasable_variant_table.subset_rows_by_position(accessible_positions)
                assert len(phasable_variant_table.variants) == len(accessible_positions)

                pedigree = create_pedigree(
                    default_gq,
                    distrust_genotypes,
                    family,
                    gl_regularizer,
                    numeric_sample_ids,
                    phasable_variant_table,
                    trios,
                )

                recombination_costs = recombination_cost_computer.compute(accessible_positions)

                # Finally, run phasing algorithm
                with timers("phase"):
                    problem_name = "MEC" if len(family) == 1 else "PedMEC"
                    logger.info(
                        "Phasing %d sample%s by solving the %s problem ...",
                        len(family),
                        plural_s(len(family)),
                        problem_name,
                    )

                    if algorithm == "hapchat":
                        dp_table = HapChatCore(all_reads)
                    else:
                        dp_table = PedigreeDPTable(
                            all_reads,
                            recombination_costs,
                            pedigree,
                            distrust_genotypes,
                            accessible_positions,
                        )

                    superreads_list, transmission_vector = dp_table.get_super_reads()
                    optimal_cost = dp_table.get_optimal_cost()
                    logger.info("%s cost: %d", problem_name, optimal_cost)

                with timers("components"):
                    master_block = None
                    heterozygous_positions_by_sample = None
                    # If we distrusted genotypes, we need to re-determine which sites are homo-/heterozygous after phasing
                    if distrust_genotypes:
                        hom_in_any_sample = set()
                        heterozygous_positions_by_sample = {}
                        heterozygous_gts = frozenset({(0, 1), (1, 0)})
                        homozygous_gts = frozenset({(0, 0), (1, 1)})
                        for sample, sample_superreads in zip(family, superreads_list):
                            hets = set()
                            for v1, v2 in zip(*sample_superreads):
                                assert v1.position == v2.position
                                if v1.position not in accessible_positions:
                                    continue
                                gt = (v1.allele, v2.allele)
                                if gt in heterozygous_gts:
                                    hets.add(v1.position)
                                elif gt in homozygous_gts:
                                    hom_in_any_sample.add(v1.position)
                            heterozygous_positions_by_sample[numeric_sample_ids[sample]] = hets
                        if len(family) > 1 and genetic_haplotyping:
                            master_block = sorted(hom_in_any_sample)
                    else:
                        if len(family) > 1 and genetic_haplotyping:
                            master_block = sorted(
                                set(homozygous_positions).intersection(set(accessible_positions))
                            )
                    overall_components = find_components(
                        accessible_positions,
                        all_reads,
                        master_block,
                        heterozygous_positions_by_sample,
                    )
                    n_phased_blocks = len(set(overall_components.values()))
                    logger.info("No. of phased blocks: %d", n_phased_blocks)
                    largest_component = find_largest_component(overall_components)
                    if len(largest_component) > 0:
                        logger.info(
                            "Largest component contains %d variants (%.1f%% of accessible variants) between position %d and %d",
                            len(largest_component),
                            len(largest_component) * 100.0 / len(accessible_positions),
                            largest_component[0] + 1,
                            largest_component[-1] + 1,
                        )

                if recombination_list_filename:
                    n_recombinations = write_recombination_list(
                        recombination_list_filename,
                        chromosome,
                        accessible_positions,
                        overall_components,
                        recombination_costs,
                        transmission_vector,
                        trios,
                    )
                    logger.info(
                        "Total no. of detected recombination events: %d", n_recombinations,
                    )

                # Superreads in superreads_list are in the same order as individuals were added to the pedigree
                for sample, sample_superreads in zip(family, superreads_list):
                    superreads[sample] = sample_superreads
                    assert len(sample_superreads) == 2
                    assert (
                        sample_superreads[0].sample_id
                        == sample_superreads[1].sample_id
                        == numeric_sample_ids[sample]
                    )
                    # identical for all samples
                    components[sample] = overall_components

                if read_list:
                    read_list.write(
                        all_reads,
                        dp_table.get_optimal_partitioning(),
                        components,
                        numeric_sample_ids,
                    )

            with timers("write_vcf"):
                logger.info("======== Writing VCF")
                changed_genotypes = vcf_writer.write(chromosome, superreads, components)
                logger.info("Done writing VCF")
                if changed_genotypes:
                    assert distrust_genotypes
                    logger.info("Changed %d genotypes while writing VCF", len(changed_genotypes))

            if gtchange_list_filename:
                logger.info("Writing list of changed genotypes to %r", gtchange_list_filename)
                write_changed_genotypes(gtchange_list_filename, changed_genotypes)

            logger.debug("Chromosome %r finished", chromosome)

    log_time_and_memory_usage(timers, show_phase_vcfs=show_phase_vcfs)


def log_best_case_phasing_info(readset, selected_reads):
    (n_best_case_blocks, n_best_case_nonsingleton_blocks,) = best_case_blocks(readset)
    (n_best_case_blocks_cov, n_best_case_nonsingleton_blocks_cov,) = best_case_blocks(
        selected_reads
    )
    logger.info(
        "Best-case phasing would result in %d non-singleton phased blocks (%d in total)",
        n_best_case_nonsingleton_blocks,
        n_best_case_blocks,
    )
    logger.info(
        "... after read selection: %d non-singleton phased blocks (%d in total)",
        n_best_case_nonsingleton_blocks_cov,
        n_best_case_blocks_cov,
    )


def raise_if_any_sample_not_in_vcf(vcf_reader, samples):
    vcf_sample_set = set(vcf_reader.samples)
    for sample in samples:
        if sample not in vcf_sample_set:
            raise CommandLineError(
                "Sample {!r} requested on command-line not found in VCF".format(sample)
            )


def setup_families(samples, ped, numeric_sample_ids, max_coverage):
    """
    Return families, family_trios pair.

    families maps a family representative to a list of family members

    family_trios maps a family representative to a list of trios in this family
    """

    # list of all trios across all families
    all_trios = dict()

    # Keep track of connected components (aka families) in the pedigree
    family_finder = ComponentFinder(samples)

    if ped:
        all_trios, pedigree_samples = setup_pedigree(ped, numeric_sample_ids, samples)
        for trio in all_trios:
            family_finder.merge(trio.father, trio.child)
            family_finder.merge(trio.mother, trio.child)

    # map family representatives to lists of family members
    families = defaultdict(list)
    for sample in samples:
        families[family_finder.find(sample)].append(sample)

    # map family representatives to lists of trios for this family
    family_trios = defaultdict(list)
    for trio in all_trios:
        family_trios[family_finder.find(trio.child)].append(trio)
    logger.info(
        "Working on %d%s samples from %d famil%s",
        len(samples),
        plural_s(len(samples)),
        len(families),
        "y" if len(families) == 1 else "ies",
    )

    largest_trio_count = max([0] + [len(trio_list) for trio_list in family_trios.values()])
    if max_coverage + 2 * largest_trio_count > 23:
        logger.warning(
            "The maximum coverage is too high! "
            "WhatsHap may take a long time to finish and require a huge amount of memory."
        )
    return families, family_trios


def find_phaseable_variants(family, include_homozygous, trios, variant_table):
    # variant indices with at least one missing genotype
    missing_genotypes = set()
    # variant indices with at least one heterozygous genotype
    heterozygous = set()
    # variant indices with at least one homozygous genotype
    homozygous = set()
    # determine which variants have missing/heterozygous/homozygous genotypes in any sample
    for sample in family:
        genotypes = variant_table.genotypes_of(sample)
        for index, gt in enumerate(genotypes):
            if gt.is_none():
                missing_genotypes.add(index)
            elif not gt.is_homozygous():
                heterozygous.add(index)
            else:
                assert gt.is_diploid_and_biallelic()
                homozygous.add(index)
    # determine which variants have Mendelian conflicts
    # variant indices with at least one Mendelian conflict
    mendelian_conflicts = find_mendelian_conflicts(trios, variant_table)
    # retain variants that are heterozygous in at least one individual (anywhere in the pedigree)
    # and do not have neither missing genotypes nor Mendelian conflicts
    if include_homozygous:
        to_retain = set(range(len(variant_table)))
    else:
        to_retain = heterozygous
    to_retain = to_retain.difference(missing_genotypes).difference(mendelian_conflicts)
    # discard every variant that is not to be retained
    to_discard = set(range(len(variant_table))).difference(to_retain)
    # Determine positions of selected variants that are homozygous in at least one individual.
    # These are used later to merge blocks containing these variants into one block (since
    # the are connected by "genetic haplotyping").
    homozygous_positions = [
        variant_table.variants[i].position for i in to_retain.intersection(homozygous)
    ]
    phasable_variant_table = deepcopy(variant_table)
    # Remove calls to be discarded from variant table
    phasable_variant_table.remove_rows_by_index(to_discard)
    logger.info(
        "Number of variants skipped due to missing genotypes: %d", len(missing_genotypes),
    )
    if len(family) == 1:
        logger.info(
            "Number of remaining%s variants: %d",
            "" if include_homozygous else " heterozygous",
            len(phasable_variant_table),
        )
    else:
        logger.info(
            "Number of variants skipped due to Mendelian conflicts: %d", len(mendelian_conflicts),
        )
        logger.info(
            "Number of remaining variants heterozygous in at least one individual: %d",
            len(phasable_variant_table),
        )
    return homozygous_positions, phasable_variant_table


def log_time_and_memory_usage(timers, show_phase_vcfs):
    total_time = timers.total()
    logger.info("\n== SUMMARY ==")
    log_memory_usage()
    # fmt: off
    logger.info("Time spent reading BAM/CRAM:                 %6.1f s", timers.elapsed("read_bam"))
    logger.info("Time spent parsing VCF:                      %6.1f s", timers.elapsed("parse_vcf"))
    if show_phase_vcfs:
        logger.info("Time spent parsing input phasings from VCFs: %6.1f s", timers.elapsed("parse_phasing_vcfs"))
    logger.info("Time spent selecting reads:                  %6.1f s", timers.elapsed("select"))
    logger.info("Time spent phasing:                          %6.1f s", timers.elapsed("phase"))
    logger.info("Time spent writing VCF:                      %6.1f s", timers.elapsed("write_vcf"))
    logger.info("Time spent finding components:               %6.1f s", timers.elapsed("components"))
    logger.info("Time spent on rest:                          %6.1f s", total_time - timers.sum())
    logger.info("Total elapsed time:                          %6.1f s", total_time)
    # fmt: on


def merge_readsets(readsets) -> ReadSet:
    all_reads = ReadSet()
    for sample, readset in readsets.items():
        for read in readset:
            assert read.is_sorted(), "Add a read.sort() here"
            all_reads.add(read)
    all_reads.sort()
    return all_reads


def create_pedigree(
    default_gq,
    distrust_genotypes,
    family,
    gl_regularizer,
    numeric_sample_ids,
    phasable_variant_table,
    trios,
):
    pedigree = Pedigree(numeric_sample_ids)
    for sample in family:
        # If distrusting genotypes, we pass genotype likelihoods on to pedigree object
        if distrust_genotypes:
            genotype_likelihoods = []
            for gt, gl in zip(
                phasable_variant_table.genotypes_of(sample),
                phasable_variant_table.genotype_likelihoods_of(sample),
            ):
                assert gt.is_diploid_and_biallelic()
                if gl is None:
                    # all genotypes get default_gq as genotype likelihood, exept the called genotype ...
                    x = [default_gq] * 3
                    # ... which gets a 0
                    x[gt.get_index()] = 0
                    genotype_likelihoods.append(PhredGenotypeLikelihoods(x))
                else:
                    genotype_likelihoods.append(gl.as_phred(regularizer=gl_regularizer))
        else:
            genotype_likelihoods = None
        pedigree.add_individual(
            sample, phasable_variant_table.genotypes_of(sample), genotype_likelihoods
        )
    for trio in trios:
        pedigree.add_relationship(father_id=trio.father, mother_id=trio.mother, child_id=trio.child)
    return pedigree


def find_mendelian_conflicts(trios, variant_table):
    mendelian_conflicts = set()
    for trio in trios:
        genotypes_mother = variant_table.genotypes_of(trio.mother)
        genotypes_father = variant_table.genotypes_of(trio.father)
        genotypes_child = variant_table.genotypes_of(trio.child)

        for index, (gt_mother, gt_father, gt_child) in enumerate(
            zip(genotypes_mother, genotypes_father, genotypes_child)
        ):
            if (not gt_mother.is_none()) and (not gt_father.is_none()) and (not gt_child.is_none()):
                if mendelian_conflict(gt_mother, gt_father, gt_child):
                    mendelian_conflicts.add(index)
    return mendelian_conflicts


def write_changed_genotypes(gtchange_list_filename, changed_genotypes):
    with open(gtchange_list_filename, "w") as f:
        print(
            "#sample", "chromosome", "position", "REF", "ALT", "old_gt", "new_gt", sep="\t", file=f,
        )
        for changed_genotype in changed_genotypes:
            print(
                changed_genotype.sample,
                changed_genotype.chromosome,
                changed_genotype.variant.position,
                changed_genotype.variant.reference_allele,
                changed_genotype.variant.alternative_allele,
                repr(changed_genotype.old_gt),
                repr(changed_genotype.new_gt),
                sep="\t",
                file=f,
            )


def write_recombination_list(
    path,
    chromosome,
    accessible_positions,
    overall_components,
    recombination_costs,
    transmission_vector,
    trios,
):
    """Return total number of recombinations"""

    transmission_vector_trio = defaultdict(list)
    for transmission_vector_value in transmission_vector:
        for trio in trios:
            value = transmission_vector_value % 4
            transmission_vector_value = transmission_vector_value // 4
            transmission_vector_trio[trio.child].append(value)
    with open(path, "w") as f:
        n = 0
        print(
            "#child_id",
            "chromosome",
            "position1",
            "position2",
            "transmitted_hap_father1",
            "transmitted_hap_father2",
            "transmitted_hap_mother1",
            "transmitted_hap_mother2",
            "recombination_cost",
            file=f,
        )
        for trio in trios:
            recombination_events = find_recombination(
                transmission_vector_trio[trio.child],
                overall_components,
                accessible_positions,
                recombination_costs,
            )
            for e in recombination_events:
                print(
                    trio.child,
                    chromosome,
                    e.position1 + 1,
                    e.position2 + 1,
                    e.transmitted_hap_father1,
                    e.transmitted_hap_father2,
                    e.transmitted_hap_mother1,
                    e.transmitted_hap_mother2,
                    e.recombination_cost,
                    file=f,
                )

            n += len(recombination_events)
    return n


# fmt: off
def add_arguments(parser):
    arg = parser.add_argument
    # Positional arguments
    arg("variant_file", metavar="VCF",
        help="VCF or BCF file with variants to be phased (can be gzip-compressed)")
    arg("phase_input_files", nargs="*", metavar="PHASEINPUT",
        help="BAM, CRAM, VCF or BCF file(s) with phase information, either through "
            "sequencing reads (BAM, CRAM) or through phased blocks (VCF, BCF)")

    arg("-o", "--output", default=sys.stdout,
        help="Output VCF file. Add .gz to the file name to get compressed output. "
            "If omitted, use standard output.")
    arg("--reference", "-r", metavar="FASTA",
        help="Reference file. Provide this to detect alleles through re-alignment. "
            "If no index (.fai) exists, it will be created")
    arg("--no-reference", action="store_true", default=False,
        help="Detect alleles without requiring a reference, at the expense of phasing quality "
             "(in particular for long reads)")
    arg("--tag", choices=("PS", "HP"), default="PS",
        help="Store phasing information with PS tag (standardized) or "
            "HP tag (used by GATK ReadBackedPhasing) (default: %(default)s)")
    arg("--output-read-list", metavar="FILE", default=None, dest="read_list_filename",
        help="Write reads that have been used for phasing to FILE.")
    arg("--algorithm", choices=("whatshap", "hapchat"), default="whatshap",
        help="Phasing algorithm to use (default: %(default)s)")

    arg = parser.add_argument_group("Input pre-processing, selection and filtering").add_argument
    arg("--merge-reads", dest="read_merging", default=False, action="store_true",
        help="Merge reads which are likely to come from the same haplotype "
        "(default: do not merge reads)")
    arg("--max-coverage", "-H", metavar="MAXCOV", type=int,
        dest="max_coverage_was_used", help=SUPPRESS)
    arg("--internal-downsampling", metavar="COVERAGE", dest="max_coverage", default=15, type=int,
        help="Coverage reduction parameter in the internal core phasing algorithm. "
            "Higher values increase runtime *exponentially* while possibly improving phasing "
            "quality marginally. Avoid using this in the normal case! (default: %(default)s)")
    arg("--mapping-quality", "--mapq", metavar="QUAL",
        default=20, type=int, help="Minimum mapping quality (default: %(default)s)")
    arg("--indels", dest="indels", default=False, action="store_true",
        help="Also phase indels (default: do not phase indels)")
    arg("--ignore-read-groups", default=False, action="store_true",
        help="Ignore read groups in BAM/CRAM header and assume all reads come "
        "from the same sample.")
    arg("--sample", dest="samples", metavar="SAMPLE", default=[], action="append",
        help="Name of a sample to phase. If not given, all samples in the "
        "input VCF are phased. Can be used multiple times.")
    arg("--chromosome", dest="chromosomes", metavar="CHROMOSOME", default=[], action="append",
        help="Name of chromosome to phase. If not given, all chromosomes in the "
        "input VCF are phased. Can be used multiple times.")

    arg = parser.add_argument_group("Read merging",
        "The options in this section are only active when --merge-reads is used").add_argument
    arg("--error-rate", dest="read_merging_error_rate",
        type=float, default=0.15,
        help="The probability that a nucleotide is wrong in read merging model "
            "(default: %(default)s).")
    arg("--maximum-error-rate", dest="read_merging_max_error_rate",
        type=float, default=0.25,
        help="The maximum error rate of any edge of the read merging graph "
        "before discarding it (default: %(default)s).")
    arg("--threshold", dest="read_merging_positive_threshold",
        type=int, default=1000000,
        help="The threshold of the ratio between the probabilities that a pair "
        "of reads come from the same haplotype and different haplotypes in the "
        "read merging model (default: %(default)s).")
    arg("--negative-threshold", dest="read_merging_negative_threshold",
        type=int, default=1000,
        help="The threshold of the ratio between the probabilities that a pair "
        "of reads come from different haplotypes and the same haplotype in the "
        "read merging model (default: %(default)s).")

    arg = parser.add_argument_group("Genotyping",
        "The options in this section require that either --distrust-genotypes or "
        "--full-genotyping is used").add_argument
    arg("--full-genotyping", dest="full_genotyping",
        action="store_true", default=False,
        help="Completely re-genotype all variants based on read data, ignores all genotype "
        "data that might be present in the VCF (EXPERIMENTAL FEATURE).")
    arg("--distrust-genotypes", dest="distrust_genotypes",
        action="store_true", default=False,
        help="Allow switching variants from hetero- to homozygous in an "
        "optimal solution (see documentation).")
    arg("--include-homozygous", dest="include_homozygous",
        action="store_true", default=False,
        help="Also work on homozygous variants, which might be turned to "
        "heterozygous")
    arg("--default-gq", dest="default_gq", type=int, default=30,
        help="Default genotype quality used as cost of changing a genotype "
        "when no genotype likelihoods are available (default %(default)s)")
    arg("--gl-regularizer", dest="gl_regularizer", type=float, default=None,
        help="Constant (float) to be used to regularize genotype likelihoods read "
        "from input VCF (default %(default)s).")
    arg("--changed-genotype-list", metavar="FILE", dest="gtchange_list_filename", default=None,
        help="Write list of changed genotypes to FILE.")

    arg = parser.add_argument_group("Pedigree phasing").add_argument
    arg("--ped", metavar="PED/FAM",
        help="Use pedigree information in PED file to improve phasing "
        "(switches to PedMEC algorithm). Columns 2, 3, 4 must refer to child, "
        "mother, and father sample names as used in the VCF and BAM/CRAM. "
        "Other columns are ignored.")
    arg("--recombination-list", metavar="FILE", dest="recombination_list_filename", default=None,
        help="Write putative recombination events to FILE.")
    arg("--recombrate", metavar="RECOMBRATE", type=float, default=1.26,
        help="Recombination rate in cM/Mb (used with --ped). If given, a constant recombination "
        "rate is assumed (default: %(default)gcM/Mb).")
    arg("--genmap", metavar="FILE",
        help="File with genetic map (used with --ped) to be used instead of constant recombination "
        "rate, i.e. overrides option --recombrate.")
    arg("--no-genetic-haplotyping", dest="genetic_haplotyping",
        action="store_false", default=True,
        help="Do not merge blocks that are not connected by reads (i.e. solely based on genotype "
        "status). Default: when in --ped mode, merge all blocks that contain at least one "
        "homozygous genotype in at least one individual into one block.")
    arg("--use-ped-samples", dest="use_ped_samples",
        action="store_true", default=False,
        help="Only work on samples mentioned in the provided PED file.")
# fmt: on


def validate(args, parser):
    if args.reference is None and not args.no_reference:
        parser.error(
            "A reference FASTA needs to be provided with -r/--reference; "
            "or use --no-reference at the expense of phasing quality."
        )
    if args.reference is not None and args.no_reference:
        parser.error("Options --reference and --no-reference cannot be used together")
    if args.ignore_read_groups and args.ped:
        parser.error("Option --ignore-read-groups cannot be used together with --ped")
    if args.genmap and not args.ped:
        parser.error("Option --genmap can only be used together with --ped")
    if args.genmap and (len(args.chromosomes) != 1):
        parser.error(
            "Option --genmap can only be used when working on exactly one "
            "chromosome (use --chromosome)"
        )
    if args.include_homozygous and not args.distrust_genotypes:
        parser.error("Option --include-homozygous can only be used with --distrust-genotypes.")
    if args.use_ped_samples and not args.ped:
        parser.error("Option --use-ped-samples can only be used when PED file is provided (--ped).")
    if args.use_ped_samples and args.samples:
        parser.error("Option --use-ped-samples cannot be used together with --samples")
    if len(args.phase_input_files) == 0 and not args.ped:
        parser.error("Not providing any PHASEINPUT files only allowed in --ped mode.")
    if args.max_coverage > 23:
        parser.error("Coverage downsampling parameter must not exceed 23.")
    if args.max_coverage_was_used is not None:
        logger.warning(
            "The --max-coverage and -H options are no longer supported. "
            "The coverage reduction parameter in the internal core phasing algorithm can now "
            "be adjusted with --internal-downsampling. Higher values increase runtime "
            "*exponentially* while possibly improving phasing quality marginally. "
            "Avoid using this in the normal case!"
        )


def main(args):
    del args.max_coverage_was_used
    del args.no_reference
    run_whatshap(**vars(args))
