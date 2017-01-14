import vcf
import csv
import os
import math


def getPos(snp):
	mapList = {'A':2, 'G':3, 'C':4, 'T':5}
	return int(mapList[snp])

chrList = {}
posList = []
fileNum = 28 
prefix = ["SRR764"] * fileNum
num = range(782, 798) + range(802, 814)
fileName = []
for i in range(0, fileNum):
	fileName.append(prefix[i] + str(num[i]) + "/output/")
	#fileName.append(prefix[i] + str(num[i]) + "/star_output/")

chrName = []
chrSnpList = {}
for i in range(1, 23):
	chrName.append('chr' + str(i))

chrName.append('chrX')

chrPosList = {}
for i in chrName:
	chrPosList.update({i:{}})

reader = vcf.Reader(filename = '../vcf_NA12878_giab/NA12878_exon.vcf')
for var in reader:
	posDict = chrPosList[var.CHROM]
	pos = int(var.POS)
	if not posDict.has_key(pos):
		ref = str(var.REF)
		alt = var.ALT
		posDict.update({pos:{'ref':ref, 'alt':alt}})


for name in fileName:
	for index in chrName:
		chrSnpList.update({index:{}})

	count_file = name + 'pileup.count'
	#count_file = name + 'pileup_30.count'
	curChr = ""
	f_out = open(name + "snp_info_tophat_30.csv", 'w')	
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
