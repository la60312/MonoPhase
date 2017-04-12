import vcf
import csv
import os
import sys
from os import listdir
from os.path import isfile, join

chr_list = {}
pos_list = {}
snp_list = {}
snp_chr_list = {}

input_dir = sys.argv[1]
snp_info = sys.argv[2]
min_count = sys.argv[3]
fc = sys.argv[4]
min_sample = sys.argv[5]

# Get mapping of gene and snp
#'../annovar/NA12878_snp_pos_info.txt'
with open(snp_info, 'rb') as f:
	reader = csv.reader(f, delimiter='\t')
	chr_name = ""
    	for row in reader:
		if chr_name != row[1]:
			if chr_name == "":
				chr_name = row[1]
			else:
				chr_list.update({chr_name: pos_list})
				pos_list = {}
				chr_name = row[1]
		if "(" in row[0]:
			gene = row[0].split("(")[0]
		else:
			gene = row[0]
		pos_list.update({int(row[2]):gene})

chr_list.update({chr_name: pos_list})

print "ucscGene complete"

input_file_list = [f for f in listdir(input_dir) if isfile(join(input_dir, f))]
input_file_list = [input_dir + '/' + fi for fi in input_file_list if fi.endswith(".binomial")]

chrMonoCountList = {}
chr_name = []                                                                                                                                              
for i in range(1, 23):
	chr_name.append('chr' + str(i))

chr_name.append('chrX')

for name in chr_name:
	chrMonoCountList.update({name:{}})

# Get the count of each snp across all samples
snp_count = {}
for input_name in input_file_list:
	with open(input_name, 'rb') as f:
		reader = csv.reader(f, delimiter=' ')
		next(reader)
		for row in reader:
			snp_count = chrMonoCountList[row[1]]
			pos = int(row[2])
			count = 0
			#if pos in snp_chr_list[row[1]]:
			if pos in snp_count:
				count = snp_count[pos]
			count = count + 1			
			snp_count.update({pos:count})

sample_snp_dict = []
for i in range(1, len(input_file_list) + 1):
	chr_dict = {}
	for name in chr_name:
		chr_dict.update({name:{}})
	
	sample_snp_dict.append(chr_dict)

chr_gene_table = {}
chr_snp_id_table = {}
for chr_index in chr_name:
	chr_gene_table.update({chr_index:{}})	
	chr_snp_id_table.update({chr_index:{}})	

# For each sample, if the snp count in total greater and equal than 5, then put into sample_snp_dict[sample][chr][gene_id]
# In sample_snp_dict[sample][chr][gene_id], is a dict to store each position pos:{ref, alt, ratio, gt}
sample_index = 0
for input_name in input_file_list:
	with open(input_name, 'rb') as f:
		reader = csv.reader(f, delimiter=' ')
		reader.next()
		for row in reader:
			snp_count = chrMonoCountList[row[1]]
			pos = int(row[2])
			count = 0
			#if pos in snp_chr_list[row[1]] and chr_list[row[1]].has_key(pos):
			if chr_list[row[1]].has_key(pos):
				gene = chr_list[row[1]][pos]
				if snp_count[pos] >= int(min_sample):
				#if snp_count[pos] >= 0:
					gt = row[6][1:-1].split(", ")
					if not sample_snp_dict[sample_index][row[1]].has_key(gene):
						sample_snp_dict[sample_index][row[1]].update({gene:{}})
					sample_snp_dict[sample_index][row[1]][gene].update({pos: {'ref':int(row[4]), 'alt':int(row[5]), 'ratio':float(row[7]), 'gt':gt}})
	
	for chr_index in chr_name:
		# For each gene, remove the gene from sample_snp_dict if contain less than 2 snp 
		# If contain at least two snp, put the sample id into chr_snp_id_table to store the sample id to match gene id 
		for gene in list(sample_snp_dict[sample_index][chr_index]):
			if len(sample_snp_dict[sample_index][chr_index][gene]) < 2:
				del sample_snp_dict[sample_index][chr_index][gene]
			else:
				if not chr_gene_table[chr_index].has_key(gene):
					chr_gene_table[chr_index].update({gene:[]})
				for snp in sample_snp_dict[sample_index][chr_index][gene].keys():
					if snp not in chr_gene_table[chr_index][gene]:
						chr_gene_table[chr_index][gene].append(snp)
					if not chr_snp_id_table[chr_index].has_key(snp):
						chr_snp_id_table[chr_index].update({snp:[]})
					chr_snp_id_table[chr_index][snp].append(sample_index)
	sample_index = sample_index + 1

# For each sample each snp, if the snp contain by less than min sample, we remove it 
for chr_index in chr_name:
	for gene in list(chr_gene_table[chr_index]):
		for snp_id in list(chr_gene_table[chr_index][gene]):
			if len(chr_snp_id_table[chr_index][snp_id]) < int(min_sample):
				for sample_index in chr_snp_id_table[chr_index][snp_id]:
					del sample_snp_dict[sample_index][chr_index][gene][snp_id]
			

sample_index = 0
for name in input_file_list:
	out_name = name + '.mono_gene'

	with open(out_name, 'wb') as f:
		writer = csv.writer(f)
		for chr_index in chr_name:
			for gene in list(sample_snp_dict[sample_index][chr_index]):
				gene_dict = {'pos':[], 'phase1':'', 'phase2':'', 'pvalue':[]}
				if len(sample_snp_dict[sample_index][chr_index][gene]) < 2:
					del sample_snp_dict[sample_index][chr_index][gene]
				else:
					for snp_pos in sorted(sample_snp_dict[sample_index][chr_index][gene].keys()):
						snp = sample_snp_dict[sample_index][chr_index][gene][snp_pos]
						hap1 = '0'
						hap2 = '0'
						cpunt = 0
						if snp['ref'] >= snp['alt']:
							hap1 = snp['gt'][0]
							hap2 = snp['gt'][1]
							count = snp['ref'] - snp['alt']	
						else:
							hap1 = snp['gt'][1]
							hap2 = snp['gt'][0]
							count = snp['alt'] - snp['ref']	
						value = snp['ratio']	
						#value = count	
						pos = gene_dict['pos']
						phase1 = gene_dict['phase1']
						phase2 = gene_dict['phase2']
						value_list = gene_dict['pvalue']
						pos.append(snp_pos)
						value_list.append(value)
						gene_dict.update({'pos':pos, 'phase1': phase1 + hap1, 'phase2':phase2 + hap2, 'pvalue':value_list})
					writer.writerow([chr_index, gene, gene_dict['pos'], gene_dict['phase1'], gene_dict['phase2'], gene_dict['pvalue']])
		sample_index = sample_index + 1

	
