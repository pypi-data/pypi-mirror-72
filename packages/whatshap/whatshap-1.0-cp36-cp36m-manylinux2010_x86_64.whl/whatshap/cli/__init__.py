import sys
import resource
import logging

from whatshap.bam import (
    AlignmentFileNotIndexedError,
    EmptyAlignmentFileError,
    SampleNotFoundError,
    ReferenceNotFoundError,
)
from whatshap.variants import ReadSetReader, ReadSetError
from whatshap.utils import IndexedFasta, FastaNotIndexedError, detect_file_format
from whatshap.core import ReadSet
from whatshap.vcf import VcfReader

logger = logging.getLogger(__name__)


class CommandLineError(Exception):
    """An anticipated command-line error occurred. This ends up as a user-visible error message"""

    pass


def open_readset_reader(*args, **kwargs):
    try:
        readset_reader = ReadSetReader(*args, **kwargs)
    except OSError as e:
        raise CommandLineError(e)
    except AlignmentFileNotIndexedError as e:
        raise CommandLineError(
            "The file '{}' is not indexed. Please create the appropriate BAM/CRAM "
            'index with "samtools index"'.format(e.args[0])
        )
    except EmptyAlignmentFileError as e:
        raise CommandLineError(
            "No reads could be retrieved from '{}'. If this is a CRAM file, possibly the "
            "reference could not be found. Try to use --reference=... or check your "
            "$REF_PATH/$REF_CACHE settings".format(e.args[0])
        )
    return readset_reader


class PhasedInputReader:
    def __init__(
        self,
        bam_or_vcf_paths,
        reference,
        numeric_sample_ids,
        ignore_read_groups,
        indels,
        **kwargs  # passed to ReadSetReader constructor
    ):
        self._bam_paths, self._vcf_paths = self._split_input_file_list(bam_or_vcf_paths)

        # TODO exit stack!
        self._numeric_sample_ids = numeric_sample_ids
        self._fasta = self._open_reference(reference) if reference else None

        vcf_readers = [VcfReader(f, indels=indels, phases=True) for f in self._vcf_paths]

        self._vcf_readers = vcf_readers
        self._ignore_read_groups = ignore_read_groups

        self._readset_reader = open_readset_reader(
            self._bam_paths, reference, numeric_sample_ids, **kwargs,
        )
        if not self._vcf_readers:
            self._vcfs = []
        else:
            self._vcfs = None  # None means uninitialized, call .read_vcf() first

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self._fasta is not None:
            self._fasta.close()

    @property
    def has_vcfs(self):
        return bool(self._vcf_paths)

    @staticmethod
    def _split_input_file_list(paths):
        bams = []
        vcfs = []
        for path in paths:
            try:
                file_format = detect_file_format(path)
            except OSError as e:
                raise CommandLineError(e)
            if file_format in ("BAM", "CRAM"):
                bams.append(path)
            elif file_format == "VCF":
                vcfs.append(path)
            else:
                raise CommandLineError("Unable to determine type of input file {!r}".format(path))
        return bams, vcfs

    @staticmethod
    def _open_reference(path):
        try:
            indexed_fasta = IndexedFasta(path)
        except OSError as e:
            raise CommandLineError("Error while opening FASTA reference file: {}".format(e))
        except FastaNotIndexedError as e:
            raise CommandLineError(
                "An index file (.fai) for the reference FASTA {!r} "
                "could not be found. Please create one with "
                '"samtools faidx".'.format(e)
            )
        return indexed_fasta

    def read_vcfs(self):
        # Read phase information provided as VCF files, if provided.
        # TODO: do this chromosome- and/or sample-wise on demand to save memory.
        self._vcfs = []
        for reader in self._vcf_readers:
            # create dict mapping chromosome names to VariantTables
            m = dict()
            logger.info("Reading phased blocks from %r", reader.path)
            for variant_table in reader:
                m[variant_table.chromosome] = variant_table
            self._vcfs.append(m)

    def read(self, chromosome, variants, sample, *, read_vcf=True, regions=None):
        """
        Return a pair (readset, vcf_source_ids) where readset is a sorted ReadSet.

        Set read_vcf to False to not read phased blocks from the VCFs
        """
        readset_reader = self._readset_reader
        for_sample = "for sample {!r} ".format(sample) if not self._ignore_read_groups else ""
        logger.info("Reading alignments %sand detecting alleles ...", for_sample)
        try:
            reference = self._fasta[chromosome] if self._fasta else None
        except KeyError:
            raise CommandLineError(
                "Chromosome {!r} present in VCF file, but not in the reference FASTA {!r}".format(
                    chromosome, self._fasta.filename
                )
            )

        bam_sample = None if self._ignore_read_groups else sample
        try:
            readset = readset_reader.read(chromosome, variants, bam_sample, reference, regions)
        except SampleNotFoundError:
            logger.warning("Sample %r not found in any BAM/CRAM file.", bam_sample)
            readset = ReadSet()
        except ReadSetError as e:
            raise CommandLineError(e)
        except ReferenceNotFoundError:
            if chromosome.startswith("chr"):
                alternative = chromosome[3:]
            else:
                alternative = "chr" + chromosome
            message = "The chromosome {!r} was not found in the BAM/CRAM file.".format(chromosome)
            if readset_reader.has_reference(alternative):
                message += " Found {!r} instead".format(alternative)
            raise CommandLineError(message)

        vcf_source_ids = set()
        if read_vcf:
            # TODO this is a bit clumsy
            if self._vcfs is None:
                raise ValueError("call PhasedInputReader.read_vcfs() first")
            # Add phasing information from VCF files, if present
            sample_id = self._numeric_sample_ids[sample]
            for i, vcf in enumerate(self._vcfs):
                if chromosome in vcf:
                    variant_table = vcf[chromosome]
                    source_id = readset_reader.n_paths + i
                    vcf_source_ids.add(source_id)
                    for read in variant_table.phased_blocks_as_reads(
                        sample, variants, source_id, sample_id
                    ):
                        readset.add(read)

        # TODO is this necessary?
        for read in readset:
            read.sort()
        readset.sort()

        logger.info(
            "Found %d reads covering %d variants", len(readset), len(readset.get_positions()),
        )
        return readset, vcf_source_ids


def log_memory_usage():
    if sys.platform == "linux":
        memory_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        logger.info("Maximum memory usage: %.3f GB", memory_kb / 1e6)
