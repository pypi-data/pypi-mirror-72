"""toil_pindel commands."""

from fnmatch import fnmatch
import os
import subprocess

from toil.common import Toil
from toil_container import ContainerArgumentParser
from toil_container import ContainerJob
import click

from toil_pindel import __version__


class StepRunner(ContainerJob):

    """Job base class used to run pindel processes."""

    def __init__(self, options, process, index=1, **kwargs):
        """
        Add the pindel process and index as attributes.

        Arguments:
            kwargs (dict): extra ContainerJob key word arguments.
            process (str): see pindel.pl --help.
            options (Namespace): toil_container options.
            index (int): possible index ranges for pindel processes are:
                input   = 1..2
                pindel  = 1..<total_refs_less_exclude>
                pin2vcf = 1..<total_refs_less_exclude>
                merge   = 1
                flag    = 1
        """
        self.index = index
        self.process = process
        runtime = kwargs.pop("runtime", options.short_job)
        memory = kwargs.pop("memory", "6G")
        cores = kwargs.pop("cores", 1)

        if not options.tgd and process in {"pin2vcf", "pindel", "input"}:
            memory = "30G"
            runtime = None

        if options.max_cores_usage:
            cores = min([options.max_cores_usage, cores])

        super(StepRunner, self).__init__(
            cores=cores,
            memory=options.max_memory_usage or memory,
            runtime=runtime,
            options=options,
            unitName="Pindel%s %s" % (process.capitalize(), index),
            displayName="Pindel%s" % process.capitalize(),
            **kwargs
        )

    def run(self, fileStore):
        """Run pindel process for a given index."""
        cmd = [
            "pindel.pl",
            "-process",
            self.process,
            "-index",
            self.index,
            "-cpus",
            self.cores,
            "-outdir",
            self.options.outdir,
            "-reference",
            self.options.reference,
            "-tumour",
            self.options.tumor_bam,
            "-normal",
            self.options.normal_bam,
            "-simrep",
            self.options.simrep,
            "-filter",
            self.options.filter,
            "-genes",
            self.options.genes,
            "-unmatched",
            self.options.unmatched,
            "-assembly",
            self.options.assembly,
            "-species",
            self.options.species,
            "-exclude",
            self.options.exclude,
        ]

        # run the command and allow file system to register output files
        cmd = list(map(str, cmd))
        self.call(cmd)


def run_toil(options):
    """Toil implementation for cgpPindel."""
    total_regions = get_total_regions(options.reference, options.exclude)
    input_step = ContainerJob(unitName="Input Base", runtime=60, options=options)
    pindel = ContainerJob(unitName="Pindel Base", runtime=60, options=options)
    pin2vcf = ContainerJob(unitName="Pin2Vcf Base", runtime=60, options=options)
    merge = StepRunner(index=1, options=options, process="merge")
    flag = StepRunner(index=1, options=options, process="flag")

    for i in [1, 2]:
        input_step.addChild(
            StepRunner(index=i, options=options, process="input", cores=4)
        )

    for i in range(1, total_regions + 1):
        pindel.addChild(StepRunner(index=i, options=options, process="pindel"))

    for i in range(1, total_regions + 1):
        pin2vcf.addChild(StepRunner(index=i, options=options, process="pin2vcf"))

    # build dag
    input_step.addFollowOn(pindel)
    pindel.addFollowOn(pin2vcf)
    pin2vcf.addFollowOn(merge)
    merge.addFollowOn(flag)

    with Toil(options) as pipe:
        if not pipe.options.restart:
            pipe.start(input_step)
        else:
            pipe.restart()


def get_parser():
    """Get pipeline configuration using toil's argparse."""
    parser = ContainerArgumentParser(version=__version__)
    parser.description = "Run toil_pindel pipeline."
    settings = parser.add_argument_group("Pipeline Settings")

    settings.add_argument(
        "--outdir",
        help="Path to putput directory.",
        required=True,
        type=click.Path(dir_okay=True, writable=True, resolve_path=True),
    )

    settings.add_argument(
        "--tumor_bam", help="Path to tumor bam file.", required=True, type=validate_bam
    )

    settings.add_argument(
        "--normal_bam",
        help="Path to normal bam file.",
        required=True,
        type=validate_bam,
    )

    settings.add_argument(
        "--species",
        choices=["HUMAN", "MOUSE"],
        help="At this point only HUMAN and MOUSE are supported.",
        required=True,
    )

    settings.add_argument("--assembly", help="Assembly name.", required=True)

    settings.add_argument(
        "--reference",
        help="Path to reference genome. Leukgen users see: GRCH37D5: "
        "/ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/genome/gr37.fasta "
        "GRCM38: "
        "/ifs/work/leukgen/ref/mus_musculus/GRCm38/genome/GRCm38.fasta",
        required=True,
        type=click.Path(file_okay=True, readable=True, resolve_path=True),
    )

    settings.add_argument(
        "--exclude",
        help="Exclude this list of ref sequences from  processing, wildcard"
        " %% - comma separated, e.g. GRCH37D5: NC_007605,hs37d5,GL%% "
        "GRCM38: JH%%,GL%%,CHR_MG%%.",
        required=False,
    )

    settings.add_argument(
        "--filter",
        help="VCF filter rules file (see FlagVcf.pl for details). This can "
        "be used the same for all species. Leukgen users see: "
        "genomic: /ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/pindel/"
        "flagging/genomicRules.lst "
        "targeted: /ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/pindel/"
        "flagging/targetedRules.lst",
        type=click.Path(file_okay=True, readable=True, resolve_path=True),
        required=True,
    )

    settings.add_argument(
        "--genes",
        help="Full path to tabix indexed coding gene footprints. Leukgen "
        "users see: GRCH37D5: /ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/"
        "vagrent/Human.GRCh37.gene_regions.bed.gz "
        "GRCM38: /ifs/work/leukgen/ref/mus_musculus/GRCm38/vagrent/"
        "gene_regions.bed.gz.",
        type=click.Path(file_okay=True, readable=True, resolve_path=True),
        required=True,
    )

    settings.add_argument(
        "--simrep",
        help="Full path to tabix indexed simple/satellite repeats. Leukgen "
        "users see: GRCH37D5: /ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/"
        "pindel/flagging/simpleRepeats.bed.gz "
        "GRCM38: /ifs/work/leukgen/ref/mus_musculus/GRCm38/pindel/flagging/"
        "simpleRepeats.bed.gz.",
        type=click.Path(file_okay=True, readable=True, resolve_path=True),
        required=True,
    )

    settings.add_argument(
        "--unmatched",
        help="Full path to tabix indexed gff3 of unmatched normal panel"
        "(see pindel_np_from_vcf.pl). Leukgen users see: "
        "GRCH37D5: /ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/pindel/"
        "unmatched_normal_panel_bwamem_mapped_with_xten/pindel_np.v4.gff3.gz "
        "GRCM38: /ifs/work/leukgen/ref/mus_musculus/GRCm38/pindel/"
        "unmatched_normal_panel_bwamem_mapped_with_xten/"
        "pindel_unmatched_normal_genomic_sw.gff.gz",
        type=click.Path(file_okay=True, readable=True, resolve_path=True),
        required=True,
    )

    settings.add_argument(
        "--max_memory_usage", help="max ram usage e.g. 1G, 1000M", default=None
    )

    settings.add_argument(
        "--max_cores_usage",
        help="limit number of available cores",
        default=None,
        type=int,
    )

    settings.add_argument(
        "--short_job", help="runtime of short jobs", default=90, required=False
    )

    settings.add_argument(
        "--tgd", help="request less resources for targeted data", action="store_true"
    )

    return parser


def process_parsed_options(options):
    """Process parsed options."""
    if options.writeLogs is not None:
        subprocess.check_call(["mkdir", "-p", options.writeLogs])
    return options


def main():
    """Parse options and run toil."""
    options = get_parser().parse_args()
    options = process_parsed_options(options=options)
    run_toil(options)


def validate_bam(value):
    """Make sure the passed bam has an index file."""
    value = os.path.abspath(value)
    index = str(value) + ".bai"

    if not os.path.isfile(index):
        raise Exception(index + " should be an existing file.")

    return value


def get_total_regions(reference, exclude):
    """Get total number of regions based on exclude string."""
    exclude = [i.replace("%", "*") for i in exclude.split(",")]
    ret = 0

    with open(reference + ".fai", "r") as f:
        for i in f:
            region = i.split("\t")[0]

            # check if no filter match the region.
            if not any(fnmatch(region, j) for j in exclude):
                ret += 1

    return ret
