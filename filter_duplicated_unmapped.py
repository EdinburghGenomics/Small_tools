import os, sys
from argparse import ArgumentParser
import pysam


def filter_duplicated_unmpped_read(input_file_path, output_file_path):
    infile = pysam.AlignmentFile(input_file_path, "rb")
    outfile = pysam.AlignmentFile(output_file_path, "wb", template=infile)
    total_reads = read_skipped = 0
    for s in infile:
        total_reads += 1
        if s.is_unmapped and not s.mate_is_unmapped and s.has_tag('BD'):
            # Skip that read
            read_skipped +=1
        else:
            outfile.write(s)
    infile.close()
    outfile.close()
    sys.stderr.write('Read %s reads from %s\n' % (total_reads, input_file_path))
    sys.stderr.write('Skipped %s reads\n' % (read_skipped))
    sys.stderr.write('Wrote %s reads to %s\n' % (total_reads - read_skipped, output_file_path))

    if os.path.exists(output_file_path):
        sys.stderr.write('Indexing %s\n' % (output_file_path))
        pysam.index(output_file_path)

    return 0


def main():
    argparser = _prepare_argparser()
    args = argparser.parse_args()
    return filter_duplicated_unmpped_read(args.input_bam_file, args.output_bam_file)


def _prepare_argparser():
    """Prepare optparser object. New arguments will be added in this
    function first.
    """
    argparser = ArgumentParser()
    argparser.add_argument("-i", "--input_bam_file", dest="input_bam_file", type=str, required = True,
                           help="The bam file containing the read to filter.")
    argparser.add_argument("-o", "--output_bam_file", dest="output_bam_file", type=str, required = True,
                           help="The bam file created after filtering .")
    return argparser

if __name__=="__main__":
    sys.exit(main())