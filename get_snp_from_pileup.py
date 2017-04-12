import vcf
import csv
import os
import math
import sys
from os import listdir
from os.path import isfile, join

def getPos(snp):
	mapList = {'A':2, 'G':3, 'C':4, 'T':5}
	return int(mapList[snp])

input_dir = sys.argv[1]
vcf_file = sys.argv[2]

input_file_list = [f for f in listdir(input_dir) if isfile(join(input_dir, f))]  
input_file_list = [input_dir + "/" + fi for fi in input_file_list if fi.endswith(".count")]       

# Chr name list init
chrName = []
for i in range(1, 23):
	chrName.append('chr' + str(i))

chrName.append('chrX')

# chr dict init
chrPosList = {}
for i in chrName:
	chrPosList.update({i:{}})

# Save all snp into dict
reader = vcf.Reader(filename = vcf_file)
for var in reader:
	posDict = chrPosList[var.CHROM]
	pos = int(var.POS)
	if not posDict.has_key(pos):
		ref = str(var.REF)
		alt = var.ALT
		posDict.update({pos:{'ref':ref, 'alt':alt}})

chrSnpList = {}
for file_name in input_file_list:
	for index in chrName:
		chrSnpList.update({index:{}})

	name = '.'.join(file_name.split('.')[:-1])
	count_file = name + '.count'

	curChr = ""
	f_out = open(name + ".snp_count.csv", 'w')	
	with open(count_file, 'rb') as f:
		reader = csv.reader(f, delimiter='\t')
		reader.next()
		for row in reader:
			posDict = chrPosList[row[0]]
			pos = int(row[1])
			if pos in posDict:
				snp = posDict[pos]
				if len(snp['alt']) > 1:
					ref = snp['alt'][0]
					alt = snp['alt'][1]
					GT = "\"[1, 2]\""
				else:
					ref = snp['ref']
					alt = snp['alt'][0]
					GT = "\"[0, 1]\""
				if len(str(alt)) > 1 or len(str(ref)) > 1:
					continue
				refCount = int(row[getPos(str(ref))])
				altCount = int(row[getPos(str(alt))])
				if refCount > 0 or altCount > 0:
					ratio = float(refCount) / float(refCount + altCount)
					f_out.write(row[0] + "," + row[1] + "," + str(ratio) + "," + str(refCount) + "," + str(altCount) + ',' + GT + "\n")
	f_out.close()
