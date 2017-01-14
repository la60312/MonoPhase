import vcf
import csv
import os
import math
import sys

min_count = sys.argv[1]
fc = sys.argv[2]
min_sample = sys.argv[3]
cmd_type = sys.argv[4]

chr_list = {}
pos_list = []
file_num = 28 
prefix = ["SRR764"] * file_num
num = range(782, 798) + range(802, 814)
file_name = []
for i in range(0, file_num):
	if cmd_type == "star":
		file_name.append(prefix[i] + str(num[i]) + "/star_output/")
	else:
		file_name.append(prefix[i] + str(num[i]) + "/output/")

chr_name = []
chr_mono_list = {}
for i in range(1, 23):
	chr_name.append('chr' + str(i))

chr_name.append('chrX')
scale = float(3) / float(16)
for name in file_name:
	for index in chr_name:
		chr_mono_list.update({index:{}})
	#if cmd_type == "sc":
	#	mono_file = name + 'mono_gene_sc_' + min_sample + '_' + min_count + '_' + fc + '.csv'
	#else:
	mono_file = name + 'mono_gene_' + min_sample + '_' + min_count + '_' + fc + '.csv'
	curChr = ""
	with open(mono_file, 'rb') as f:
		reader = csv.reader(f, delimiter=',')
		for row in reader:
			posDict = chr_mono_list[row[0]]
			posStr = row[2][1:-1].split(", ")
			valueStr = row[5][1:-1].split(", ")
			for i in range(0, len(posStr)):
				info = [int(posStr[i]), row[3][i], row[4][i], int(posStr[0]), float(valueStr[i])]
				posDict.update({posStr[i]: info})
			chr_mono_list.update({row[0]:posDict})	

	#if cmd_type == "sc":
	#	f = open(name + 'mono_phased_sc_' + min_sample + '_' + min_count + '_' + fc + '.vcf', 'w')
	#else:
	f = open(name + 'mono_phased_' + min_sample + '_' + min_count + '_' + fc + '.vcf', 'w')

	f.write("##contig=<ID=chr1,length=249250621>\n")
	f.write("##contig=<ID=chr2,length=243199373>\n")
	f.write("##contig=<ID=chr3,length=198022430>\n")
	f.write("##contig=<ID=chr4,length=191154276>\n")
	f.write("##contig=<ID=chr5,length=180915260>\n")
	f.write("##contig=<ID=chr6,length=171115067>\n")
	f.write("##contig=<ID=chr7,length=159138663>\n")
	f.write("##contig=<ID=chr8,length=146364022>\n")
	f.write("##contig=<ID=chr9,length=141213431>\n")
	f.write("##contig=<ID=chr10,length=135534747>\n")
	f.write("##contig=<ID=chr11,length=135006516>\n")
	f.write("##contig=<ID=chr12,length=133851895>\n")
	f.write("##contig=<ID=chr13,length=115169878>\n")
	f.write("##contig=<ID=chr14,length=107349540>\n")
	f.write("##contig=<ID=chr15,length=102531392>\n")
	f.write("##contig=<ID=chr16,length=90354753>\n")
	f.write("##contig=<ID=chr17,length=81195210>\n")
	f.write("##contig=<ID=chr18,length=78077248>\n")
	f.write("##contig=<ID=chr19,length=59128983>\n")
	f.write("##contig=<ID=chr20,length=63025520>\n")
	f.write("##contig=<ID=chr21,length=48129895>\n")
	f.write("##contig=<ID=chr22,length=51304566>\n")
	f.write("##contig=<ID=chrX,length=155270560>\n")
	f.write("##FILTER=<ID=Uncertain,Description=\"Uncertain genotype due to reason in filter INFO field\">\n")
	f.write("##FORMAT=<ID=PS,Number=1,Type=Integer,Description=\"RTG Phase set for the genotype\">\n")
	f.write("##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Net Genotype across all datasets\">\n")
	f.write("##FORMAT=<ID=PQ,Number=1,Type=Integer,Description=\"Phase quality\">\n")
	f.write("#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO    FORMAT  NA12878\n")
	
	#if cmd_type == "sc":
	#	reader = vcf.Reader(filename = 'sc_data.vcf')
	#else:
	reader = vcf.Reader(filename = '../vcf_NA12878_giab/NA12878_exon.vcf')
	for var in reader:
		posDict = chr_mono_list[var.CHROM]
		pos = str(var.POS)
		if posDict.has_key(pos):
			GT = posDict[pos][1] + '|' + posDict[pos][2]
			PS = str(posDict[pos][3])
			qual = int(-10 * (math.log10(posDict[pos][4] + 0.0000000000000001)))
			#qual = int((-10 * (math.log10(posDict[pos][4] + 0.0000000000000001))) * scale + 30)
			#qual = posDict[pos][4]
			altList = str(var.ALT)[1:-1].split(", ")
			alt = altList[0]
			if len(altList) > 1:
				for i in range(1, len(altList)):
					alt = alt + "," + altList[i] 
			f.write(str(var.CHROM) + '\t' + str(var.POS) + '\t' + '.' + '\t' + str(var.REF) + '\t' + alt + '\t' + str(var.QUAL) + '\t' + '.' + '\t' + '.' + '\t' + 'GT:PS' + '\t' + GT + ':' + PS + "\n")
			#f.write(str(var.CHROM) + '\t' + str(var.POS) + '\t' + '.' + '\t' + str(var.REF) + '\t' + alt + '\t' + str(var.QUAL) + '\t' + '.' + '\t' + '.' + '\t' + 'GT:PS:PQ' + '\t' + GT + ':' + PS + ':' + str(qual) + "\n")

	f.close()	
	print name
