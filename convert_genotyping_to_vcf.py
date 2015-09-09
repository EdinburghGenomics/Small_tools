from argparse import ArgumentParser
from collections import defaultdict
import csv

__author__ = 'tcezard'

SNPs_definition = {"C___2728408_10": ["rs3010325",  "1",  "59569829",  "C", "Reverse"],
                   "C___1563023_10": ["rs2136241",  "1",  "163289571", "C", "Reverse"],
                   "C__15935210_10": ["rs2259397",  "1",  "208068579", "T", "Reverse"],
                   "C__33211212_10": ["rs7564899",  "2",  "11200347",  "G", "Forward"],
                   "C___3227711_10": ["rs4971536",  "2",  "21084332",  "C", "Reverse"],
                   "C__30044763_10": ["rs10194978", "2",  "50525067",  "G", "Forward"],
                   "C__11821218_10": ["rs4855056",  "3",  "181638250", "A", "Forward"],
                   "C___1670459_10": ["rs6554653",  "5",  "11870138",  "C", "Reverse"],
                   "C__29619553_10": ["rs9396715",  "6",  "9914294",   "T", "Reverse"],
                   "C___1007630_10": ["rs441460",   "6",  "25548288",  "G", "Reverse"],
                   "C__26546714_10": ["rs7773994",  "6",  "37572144",  "T", "Forward"],
                   "C___7421900_10": ["rs1415762",  "6",  "125039942", "C", "Forward"],
                   "C__27402849_10": ["rs6927758",  "6",  "163719115", "C", "Reverse"],
                   "C___2953330_10": ["rs7796391",  "7",  "126113335", "A", "Reverse"],
                   "C__16205730_10": ["rs2336695",  "8",  "1033625",   "A", "Forward"],
                   "C___8850710_10": ["rs1157213",  "8",  "104215466", "T", "Forward"],
                   "C___1801627_20": ["rs10869955", "9",  "80293657",  "C", "Reverse"],
                   "C___7431888_10": ["rs1533486",  "10", "1511786",   "T", "Forward"],
                   "C___1250735_20": ["rs4751955",  "10", "117923225", "A", "Forward"],
                   "C___1902433_10": ["rs10771010", "12", "23769449",  "T", "Forward"],
                   "C__31386842_10": ["rs12318959", "12", "28781965",  "C", "Reverse"],
                   "C__26524789_10": ["rs3742257",  "13", "43173198",  "T", "Forward"],
                   "C___8924366_10": ["rs1377935",  "14", "25843774",  "T", "Reverse"],
                   "C_____43852_10": ["rs946065",   "14", "55932919",  "C", "Forward"],
                   "C__11522992_10": ["rs6598531",  "15", "99130113",  "T", "Forward"],
                   "C__10076371_10": ["rs4783229",  "16", "82622140",  "T", "Reverse"],
                   "C___7457509_10": ["rs1567612",  "18", "35839365",  "G", "Forward"],
                   "C___1122315_10": ["rs11660213", "18", "42481985",  "A", "Reverse"],
                   "C__11710129_10": ["rs11083515", "19", "39697974",  "A", "Forward"],
                   "C___1027548_20": ["rs768983",   "Y",  "6818291",   "C",  "Reverse"],
                   "C___8938211_20": ["rs3913290",  "Y",  "8602518",   "C",  "Forward"],
                   "C___1083232_10": ["rs2032598",  "Y",  "14850341",  "T",  "Reverse"]}


HEADERS_SAMPLE_ID="Sample Id"
HEADERS_PLATE_BARCODE="Plate Barcode"
HEADERS_ASSAY_NAME="Assay Name"
HEADERS_ASSAY_ID="Assay ID"
HEADERS_CALL="Call"

vcf_header=['#CHROM','POS','ID','REF','ALT','QUAL','FILTER','INFO','FORMAT']

_complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
def complement(bases):
    return ''.join([_complement.get(base) for base in bases])

def get_genotype_from_call(ref_allele, call, design_strand):
    """Uses the SNPs definition to convert the genotype call to a vcf compatible genotype"""
    alternate_allele = '.'
    genotype = './.'
    if call == 'Undefined':
        return alternate_allele, genotype
    if design_strand == 'Reverse':
        call = complement(call)
    callset = set(call)
    if ref_allele in callset and len(callset) == 1:
        genotype='0/0'
    elif ref_allele in callset and len(callset) == 2:
        genotype='0/1'
        callset.remove(ref_allele)
        alternate_allele = ','.join(callset)
    elif not ref_allele in callset and len(callset) == 1:
        genotype='1/1'
        alternate_allele = ','.join(callset)
    return alternate_allele, genotype

def vcf_header_from_fai_file(genome_fai):
    """Generate a vcf header from an fai file"""
    header_entries = []
    with open(genome_fai) as open_file:
        reader = csv.reader(open_file, delimiter='\t')
        for row in reader:
            header_entries.append('##contig=<ID=%s,length=%s>'%(row[0], row[1]))
    return header_entries

def order_from_fai(all_records, genome_fai):
    ordered_records = []
    with open(genome_fai) as open_file:
        reader = csv.reader(open_file, delimiter='\t')
        for row in reader:
            snps = all_records.get(row[0], [])
            #Sort the SNPs by position within a ref
            snps.sort(key=lambda snp: int(snp[1]))
            #convert the array to str
            ordered_records.extend(['\t'.join(s) for s in snps])
    return ordered_records

def convert_genotype_csv(csv_file, genome_fai, flank_length=0):
    with open(csv_file) as open_file:
        reader = csv.DictReader(open_file, delimiter='\t')
        all_records = defaultdict(list)
        for line in reader:
            sample = line[HEADERS_SAMPLE_ID]
            assay_id = line[HEADERS_ASSAY_ID]
            SNPs_id, reference_name, reference_position, ref_allele, design_strand = SNPs_definition.get(assay_id)
            alt_allele, genotype = get_genotype_from_call(ref_allele, line.get(HEADERS_CALL), design_strand)
            if flank_length:
                out=[assay_id, str(flank_length+1), SNPs_id, ref_allele, alt_allele, ".", ".", ".", "GT", genotype]
            else:
                out=[reference_name, reference_position, SNPs_id, ref_allele, alt_allele, ".", ".", ",", "GT", genotype]
            all_records[out[0]].append(out)
    all_lines = ["##fileformat=VCFv4.1",
                 '##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">']
    all_lines.extend(vcf_header_from_fai_file(genome_fai))
    vcf_header.append(sample)
    all_lines.append('\t'.join(vcf_header))
    all_lines.extend(order_from_fai(all_records, genome_fai))
    return '\n'.join(all_lines)

def main():
    argparser = _prepare_argparser()
    args = argparser.parse_args()
    with open(args.output_file, 'w') as open_ouput:
        text = convert_genotype_csv(args.genotype_file, args.reference_fai, args.flanking_size)
        open_ouput.write(text)

def _prepare_argparser():
    """Prepare optparser object. New arguments will be added in this
    function first.
    """
    description = """Convert genotype file to vcf for comparison"""

    argparser = ArgumentParser(description=description)

    argparser.add_argument("-g", "--genotype_file", dest="genotype_file", type=str, required = True,
                           help="The genotype file to convert.")
    argparser.add_argument("-r", "--reference_fai", dest="reference_fai", type=str, required = True,
                           help="The file containing the reference fai.")
    argparser.add_argument("-f", "--flanking_size", dest="flanking_size", type=int,
                           help="The size of the flanking region used to build the small genome.")
    argparser.add_argument("-o", "--output_file", dest="output_file", type=str, required = True,
                           help="The output file name.")
    return argparser

if __name__=="__main__":
    main()