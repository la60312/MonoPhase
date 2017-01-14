import vcf
import csv
import os
import collections

chrList = {}
posList = []
fileNum = 28 
prefix = ["SRR764"] * fileNum
num = range(782, 798) + range(802, 814)
fileName = []
for i in range(0, fileNum):
	fileName.append(prefix[i] + str(num[i]))

chrIndex = ["chr"] *22
for i in range(1, 23):
	chrList.update({"chr"+str(i):{}})

chrList.update({"chrX":{}})

for i in range(1, 23):
	chrIndex[i - 1] = chrIndex[i - 1] + str(i)

chrIndex.append("chrX")

index = 0 
for name in fileName:
	vcfFile = name + '/star_output/snp_info_star_30.csv'
	print "start read vcf:" + vcfFile
	with open(vcfFile, 'rb') as f:
		reader = csv.reader(f, delimiter=',')
		chrName = ""
	        for row in reader:
			if row[0] != chrName:
				chrName = row[0]
				var_dict = chrList[chrName]
			alt = row[4]
			ref = row[3]
			if int(row[1]) in var_dict:
				pos_list = var_dict[int(row[1])]
				pos_list.append({'ref':ref, 'alt':alt, 'ratio':float(ref)/float(ref + alt),'sample':index})
				var_dict.update({int(row[1]):pos_list})
			else:
				pos_list = []
				pos_list.append({'ref':ref, 'alt':alt, 'ratio':float(ref)/float(ref + alt),'sample':index})
				var_dict.update({int(row[1]):pos_list})
	index = index + 1
				
	
with open('star_total_ref_count.csv', 'wb') as f:  # Just use 'w' mode in 3.x
	writer = csv.writer(f)
	for i in chrIndex:
		var_dict = chrList[i]
		od = collections.OrderedDict(sorted(var_dict.items()))
		for k, v in od.items():
			if v != []:
				ref = [0] * 28
				for s in v:
					ref[s['sample']] = int(s['ref'])
				out = [i, k]
				for count in ref:
					out.append(count)
				writer.writerow(out)


with open('star_total_alt_count.csv', 'wb') as f:  # Just use 'w' mode in 3.x
	writer = csv.writer(f)
	for i in chrIndex:
		var_dict = chrList[i]
		od = collections.OrderedDict(sorted(var_dict.items()))
		for k, v in od.items():
			if v != []:
				alt = [0] * 28
				for s in v:
					alt[s['sample']] = int(s['alt'])
				out = [i, k]
				for count in alt:
					out.append(count)
				writer.writerow(out)
