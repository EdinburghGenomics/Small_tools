import os
from unittest.case import TestCase
from convert_genotyping_to_vcf import convert_genotype_csv

__author__ = 'tcezard'


class Test_small_tools(TestCase):
    def setUp(self):
        self.genotype_csv = os.path.join(os.path.dirname(__file__), 'test_data','E03159_WGS_32_panel_9504430.csv')
        self.genotype_csv = os.path.join(os.path.dirname(__file__), 'test_data','E03159_WGS_32_panel.csv')
        self.small_reference_fai = os.path.join(os.path.dirname(__file__), 'test_data','genotype_32_SNPs_genome_600bp.fa.fai')
        self.reference_fai = os.path.join(os.path.dirname(__file__), 'test_data','GRCh37.fa.fai')



    def test_convert_genotype_csv(self):
        vcf_text = """#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	50293
1	163289571	rs2136241	C	T	.	.	GT	1/1
1	208068579	rs2259397	T	A	.	.	GT	1/1
1	59569829	rs3010325	C	T	.	.	GT	0/1
10	117923225	rs4751955	A	.	.	.	GT	./.
10	1511786	rs1533486	T	G	.	.	GT	0/1
12	23769449	rs10771010	T	C	.	.	GT	1/1
12	28781965	rs12318959	C	.	.	.	GT	./.
13	43173198	rs3742257	T	.	.	.	GT	0/0
14	25843774	rs1377935	T	.	.	.	GT	0/0
14	55932919	rs946065	C	.	.	.	GT	./.
15	99130113	rs6598531	T	.	.	.	GT	0/0
16	82622140	rs4783229	T	C	.	.	GT	0/1
18	35839365	rs1567612	G	A	.	.	GT	0/1
18	42481985	rs11660213	A	G	.	.	GT	0/1
19	39697974	rs11083515	A	G	.	.	GT	1/1
2	11200347	rs7564899	G	A	.	.	GT	0/1
2	21084332	rs4971536	C	.	.	.	GT	0/0
2	50525067	rs10194978	G	A	.	.	GT	0/1
3	181638250	rs4855056	A	G	.	.	GT	0/1
5	11870138	rs6554653	C	T	.	.	GT	1/1
6	125039942	rs1415762	C	.	.	.	GT	0/0
6	163719115	rs6927758	C	.	.	.	GT	./.
6	25548288	rs441460	G	A	.	.	GT	1/1
6	37572144	rs7773994	T	.	.	.	GT	0/0
6	9914294	rs9396715	T	.	.	.	GT	0/0
7	126113335	rs7796391	A	G	.	.	GT	1/1
8	1033625	rs2336695	A	G	.	.	GT	1/1
8	104215466	rs1157213	T	C	.	.	GT	0/1
9	80293657	rs10869955	C	A	.	.	GT	0/1
Y	14850341	rs2032598	T	.	.	.	GT	./.
Y	6818291	rs768983	C	.	.	.	GT	./.
Y	8602518	rs3913290	C	.	.	.	GT	./."""
        #text=convert_genotype_csv(self.genotype_csv,self.reference_fai)
        #print(text)
        #self.assertEqual(text,vcf_text)

        text=convert_genotype_csv(self.genotype_csv, self.small_reference_fai, 600)

        print(text)