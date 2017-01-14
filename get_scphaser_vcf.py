import vcf
import csv
import os
import math
import sys

min_count = sys.argv[1]
fc = sys.argv[2]
min_sample = sys.argv[3]
data_src = sys.argv[4]

prefix = ""
if data_src == "star":
	prefix = "star_scphaser/scphaser_star_"
else:
	prefix = "tophat_scphaser/scphaser_tophat_"
	
chrList = {}
posList = []

allList = []
allFilterList = []
chrName = []
chrMonoList = {}

input_type = ['ac', 'gt']
weight = ['TRUE', 'FALSE']
method = ['exaust', 'pam']

chr_name = []
chr_mono_list = {}
for i in range(1, 23):
	chr_name.append('chr' + str(i))

chr_name.append('chrX')

# For loop to run all 8 settings
for method_index in range(0, 2):
	for type_index in range(0, 2):
		for weight_index in range(0, 2):
			mono_file = prefix + method[method_index] + "_" + input_type[type_index] + "_" + weight[weight_index] + "_" + min_sample + "_" + min_count + "_" + fc +".csv"
			curChr = ""
			for index in chr_name:
				chr_mono_list.update({index:{}})
			geneDict = {}
			with open(mono_file, 'rb') as fr:
				reader = csv.reader(fr, delimiter='\t')
				for row in reader:
					if geneDict.has_key(row[2]):
						PS = geneDict[row[2]]
						info = [row[8], PS]
					else:
						PS = str(row[1])
						geneDict.update({row[2]:int(row[1])})
						info = [row[8], PS]
					posDict = chr_mono_list[row[0]]
					posDict.update({row[1]: info})
					chr_mono_list.update({row[0]:posDict})	

			f = open(prefix + method[method_index] + "_" + input_type[type_index] + "_" + weight[weight_index] + "_" + min_sample + "_" + min_count + "_" + fc + ".vcf", 'w')
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
			f.write("#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO    FORMAT  NA12878\n")
			
			#mono_file = prefix + method[method_index] + "_" + input_type[type_index] + "_" + weight[weight_index] + "_" + min_sample + "_" + min_count + "_" + fc +".csv"
			#curChr = ""
			#with open(mono_file, 'rb') as fr:
			reader = vcf.Reader(filename = '../vcf_NA12878_giab/NA12878_exon.vcf')
			for var in reader:
				posDict = chr_mono_list[var.CHROM]
				pos = str(var.POS)
				altList = str(var.ALT)[1:-1].split(", ")
				alt = altList[0]
				if len(altList) > 1:
					for i in range(1, len(altList)):
						alt = alt + "," + altList[i] 
				if posDict.has_key(pos):

				#for row in reader:
			#		if curGene == "":
			#			curGene = row[2]
			#			PS = str(row[1])
			#		if curGene != row[2]:
			#			curGene = row[2]
			#			PS = str(row[1])
					f.write(var.CHROM + '\t' + pos + '\t' + '.' + '\t' + str(var.REF) + '\t' + alt + '\t50' + '\t' + '.' + '\t' + '.' + '\t' + 'GT:PS' + '\t' + str(posDict[pos][0]) + ':' + str(posDict[pos][1]) + "\n")
			
			f.close()	
