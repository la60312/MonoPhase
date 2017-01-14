import vcf
import sys

file1 = sys.argv[1]
file2 = sys.argv[2]
outName = sys.argv[3]

class chromosome:
	def __init__(self):
		self.chrName = "" 
		self.hetNum = 0
		self.varNum = 0
		self.blockNum = 0
		self.phasePairNum = 0
		self.switchErrNum = 0
		self.switchErrRate = "0.0"
		self.largestPairNum = 0
		self.largestSwitchErrNum = 0
		self.largestSwitchErrRate = "0.0"

#init list
chrList = []
for i in range(0, 24):
	chrList.append(chromosome())

#Read file
chrNum = -1
#resultFile = open("scphaser.compare","r")
#resultFile = open("scphaser_our_data_phased.vcf.compare","r")
#resultFile = open("results/exp_phased_1_3_cutoff_5_new.vcf.compare", "r")
resultFile = open(file1, "r")
line = resultFile.readline()
while line != "":
	print line
	if("- Chromosome" in line):
		chrName = line.split()[2]
		chrNum = chrName.split("r")[1]
		if(chrNum == "X"):
			chrNum = 23
		if(chrNum == "Y"):
			chrNum = 24
		chrNum = int(chrNum) - 1
		chrList[chrNum].chrName = chrName
	if("common heterozygous variants" in line):
		chrList[chrNum].hetNum = int(line.split(":")[1].split()[0])
	if("non-singleton intersection blocks" in line):
		chrList[chrNum].blockNum = int(line.split(":")[1].split()[0])
		line = resultFile.readline()
		chrList[chrNum].varNum = int(line.split(":")[1].split()[0])
	if("ALL INTERSECTION BLOCKS:" in line):
		line = resultFile.readline()
		chrList[chrNum].phasePairNum = int(line.split(":")[1].split()[0])
		line = resultFile.readline()
		chrList[chrNum].switchErrNum = int(line.split(":")[1].split()[0])
		line = resultFile.readline()
		chrList[chrNum].switchErrRate = line.split(":")[1].split("%")[0]
	if("LARGEST INTERSECTION BLOCK:" in line):
		line = resultFile.readline()
		chrList[chrNum].largestPairNum = int(line.split(":")[1].split()[0])
		line = resultFile.readline()
		chrList[chrNum].largestSwitchErrNum = int(line.split(":")[1].split()[0])
		line = resultFile.readline()
		chrList[chrNum].largestSwitchErrRate = line.split(":")[1].split("%")[0]
	line = resultFile.readline()

resultFile.close()

chrList2 = []
for i in range(0, 24):
	chrList2.append(chromosome())

chrNum = -1
#resultFile = open("results/star_exp_phased_1_3_cutoff_5.vcf.compare", "r")
resultFile = open(file2, "r")
line = resultFile.readline()
while line != "":
	print line
	if("- Chromosome" in line):
		chrName = line.split()[2]
		chrNum = chrName.split("r")[1]
		if(chrNum == "X"):
			chrNum = 23
		if(chrNum == "Y"):
			chrNum = 24
		chrNum = int(chrNum) - 1
		chrList2[chrNum].chrName = chrName
	if("common heterozygous variants" in line):
		chrList2[chrNum].hetNum = int(line.split(":")[1].split()[0])
	if("non-singleton intersection blocks" in line):
		chrList2[chrNum].blockNum = int(line.split(":")[1].split()[0])
		line = resultFile.readline()
		chrList2[chrNum].varNum = int(line.split(":")[1].split()[0])
	if("ALL INTERSECTION BLOCKS:" in line):
		line = resultFile.readline()
		chrList2[chrNum].phasePairNum = int(line.split(":")[1].split()[0])
		line = resultFile.readline()
		chrList2[chrNum].switchErrNum = int(line.split(":")[1].split()[0])
		line = resultFile.readline()
		chrList2[chrNum].switchErrRate = line.split(":")[1].split("%")[0]
	if("LARGEST INTERSECTION BLOCK:" in line):
		line = resultFile.readline()
		chrList2[chrNum].largestPairNum = int(line.split(":")[1].split()[0])
		line = resultFile.readline()
		chrList2[chrNum].largestSwitchErrNum = int(line.split(":")[1].split()[0])
		line = resultFile.readline()
		chrList2[chrNum].largestSwitchErrRate = line.split(":")[1].split("%")[0]
	line = resultFile.readline()

resultFile.close()


avgErrNum1 = 0
avgErrNum2 = 0
avgPairNum1 = 0
avgPairNum2 = 0
avgErrRate1 = 0.0
avgErrRate2 = 0.0
avgVarNum1 = 0
avgVarNum2 = 0
avgTotalVar = 0.0
totalBlock1 = 0
totalBlock2 = 0

for i in range(0, 23):
	avgErrNum1 = avgErrNum1 + int(chrList[i].switchErrNum)
	avgErrNum2 = avgErrNum2 + int(chrList2[i].switchErrNum)
	avgPairNum1 = avgPairNum1 + float(chrList[i].phasePairNum)
	avgPairNum2 = avgPairNum2 + float(chrList2[i].phasePairNum)
	avgErrRate1 = avgErrRate1 + float(chrList[i].switchErrRate)
	avgErrRate2 = avgErrRate2 + float(chrList2[i].switchErrRate)
	avgVarNum1 = avgVarNum1 + float(chrList[i].varNum)
	avgVarNum2 = avgVarNum2 + float(chrList2[i].varNum)
	avgTotalVar = avgTotalVar + float(chrList[i].hetNum)
	totalBlock1 = totalBlock1 + float(chrList[i].blockNum)
	totalBlock2= totalBlock2 + float(chrList2[i].blockNum)


print avgErrNum1
print avgErrNum2
print avgPairNum1
print avgPairNum2
print totalBlock1
print totalBlock2

avgErrRate1 = round(float(avgErrNum1) / float(avgPairNum1), 5) * 100
avgErrRate2 = round(float(avgErrNum2) / float(avgPairNum2), 5) * 100
avgErrNum1 = round(float(avgErrNum1) / float(23.0), 3)
avgErrNum2 = round(float(avgErrNum2) / float(23.0), 3)




#avgErrRate1 = round(float(avgErrRate1) / float(23.0), 3)
#avgErrRate2 = round(float(avgErrRate2) / float(23.0), 3)
avgVarNum1 = round(float(avgVarNum1) / float(23.0), 3)
avgVarNum2 = round(float(avgVarNum2) / float(23.0), 3)
avgTotalVar = round(float(avgTotalVar) / float(23.0), 3)


exon_list = []
currentChr = "chr1"
vcf_file = '../vcf_NA12878_giab/NA12878_exon.vcf'
reader = vcf.Reader(filename = vcf_file)
count = 0
for var in reader:
	if var.CHROM != currentChr:
		exon_list.append(count)
		currentChr = var.CHROM
		count = 0
	count = count + 1

exon_list.append(count)






#Output text
outFile = open('table_result/' + outName,"w")
outFile.write("\\documentclass[10pt, a4paper]{article}\n")
outFile.write("\\usepackage{multirow}\n")
outFile.write("\\usepackage[margin=1 in]{geometry}\n")
outFile.write("\\begin{document}\n")
outFile.write("\\begin{center}\n")
outFile.write("\\begin{table}[ht]\n")
outFile.write("\\caption{Result for scphasr and whatshap, both use star data}\\medskip\n")
outFile.write("\\label{compare}\n")
#outFile.write("\\begin{minipage}{\\textwidth}\n")
outFile.write("\\noindent\n")
outFile.write("\\begin{tabular}{|c|c|c|c|c|c|c|c|} \\hline\n")
outFile.write("\\multirow{2}{*}{chr}& \\multicolumn{2}{c|}{Switch error}& \\multicolumn{2}{c|}{Switch error(\%)}&\\multicolumn{2}{c|}{variants}&\\multirow{2}{*}{Exon Variants} \\\\ \n")
outFile.write("& scphaser& whatshap& scphaser& whatshap&scphaser&whatshap& \\\\ \\hline \n")


#print table content
for i in range(0, 23):
	bfText1 = ""
	bfText2 = ""
	if(float(chrList[i].switchErrRate) < float(chrList2[i].switchErrRate)):
		bfText1 = "\\bf{" + chrList[i].switchErrRate + "}"
		bfText2 = chrList2[i].switchErrRate
	elif(float(chrList[i].switchErrRate) > float(chrList2[i].switchErrRate)):
		bfText1 = chrList[i].switchErrRate
		bfText2 = "\\bf{" + chrList2[i].switchErrRate + "}"	
	else:
		bfText1 = "\\bf{" + chrList[i].switchErrRate + "}"
		bfText2 = "\\bf{" + chrList2[i].switchErrRate + "}"	
	bfVar1 = ""
	bfVar2 = ""
	if(chrList[i].varNum > chrList2[i].varNum):
		bfVar1 = "\\bf{" + str(chrList[i].varNum) + "}"
		bfVar2 = str(chrList2[i].varNum)
	elif(chrList[i].varNum < chrList2[i].varNum):
		bfVar1 = str(chrList[i].varNum)
		bfVar2 = "\\bf{" + str(chrList2[i].varNum) + "}"
	else:
		bfVar1 = "\\bf{" + str(chrList[i].varNum) + "}"
		bfVar2 = "\\bf{" + str(chrList2[i].varNum) + "}"

	text = chrList[i].chrName + "&" + str(chrList[i].switchErrNum) + "&" + str(chrList2[i].switchErrNum) + "&" + bfText1 + "&" + bfText2 + "&" + bfVar1 + "&" + bfVar2 + "&" + str(exon_list[i])+ "\\\\ \\hline \n"
	outFile.write(text)

bfText1 = ""
bfText2 = ""
if(avgErrRate1 < avgErrRate2):
	bfText1 = "\\bf{" + str(avgErrRate1) + "}"
	bfText2 = str(avgErrRate2)
elif(avgErrRate1 > avgErrRate2):
	bfText1 = str(avgErrRate1)
	bfText2 = "\\bf{" + str(avgErrRate2) + "}"	
else:
	bfText1 = "\\bf{" + str(avgErrRate1) + "}"
	bfText2 = "\\bf{" + str(avgErrRate2) + "}"
bfVar1 = ""
bfVar2 = ""
if(avgVarNum1 > avgVarNum2):
	bfVar1 = "\\bf{" + str(avgVarNum1) + "}"
	bfVar2 = str(avgVarNum2)
elif(avgVarNum1 < avgVarNum2):
	bfVar1 = str(avgVarNum1)
	bfVar2 = "\\bf{" + str(avgVarNum2) + "}"	
else:
	bfVar1 = "\\bf{" + str(avgVarNum1) + "}"
	bfVar2 = "\\bf{" + str(avgVarNum2) + "}"	
text = "Avg" + "&" + str(avgErrNum1) + "&" + str(avgErrNum2) + "&" + bfText1 + "&" + bfText2 + "&" + bfVar1 + "&" + bfVar2 + "&" + "\\\\ \\hline \n"
outFile.write(text)
outFile.write("\\end{tabular}\n")
#outFile.write("\\end{minipage}\n")
outFile.write("\\end{table}\n")
outFile.write("\\end{center}\n")
outFile.write("\\begin{center}\n")

outFile.write("\\begin{table}[ht]\n")
outFile.write("\\caption{Result for scphasr and whatshap, both use tophat data}\\medskip\n")
outFile.write("\\label{compare}\n")
#outFile.write("\\begin{minipage}{\\textwidth}\n")
outFile.write("\\noindent\n")
outFile.write("\\begin{tabular}{|c|c|c|c|c|c|c|c|} \\hline\n")
outFile.write("\\multirow{2}{*}{chr}& \\multicolumn{2}{c|}{Switch error}& \\multicolumn{2}{c|}{Switch error(\%)}&\\multicolumn{2}{c|}{variants}&\\multirow{2}{*}{Exon Variants} \\\\ \n")
outFile.write("& scphaser& whatshap& scphaser& whatshap&scphaser&whatshap& \\\\ \\hline \n")


#print table content
if(avgErrRate1 < avgErrRate2):
	bfText1 = "\\bf{" + str(avgErrRate1) + "}"
	bfText2 = str(avgErrRate2)
elif(avgErrRate1 > avgErrRate2):
	bfText1 = str(avgErrRate1)
	bfText2 = "\\bf{" + str(avgErrRate2) + "}"	
else:
	bfText1 = "\\bf{" + str(avgErrRate1) + "}"
	bfText2 = "\\bf{" + str(avgErrRate2) + "}"
bfVar1 = ""
bfVar2 = ""
if(avgVarNum1 > avgVarNum2):
	bfVar1 = "\\bf{" + str(avgVarNum1) + "}"
	bfVar2 = str(avgVarNum2)
elif(avgVarNum1 < avgVarNum2):
	bfVar1 = str(avgVarNum1)
	bfVar2 = "\\bf{" + str(avgVarNum2) + "}"	
else:
	bfVar1 = "\\bf{" + str(avgVarNum1) + "}"
	bfVar2 = "\\bf{" + str(avgVarNum2) + "}"	
text = "Avg" + "&" + str(avgErrNum1) + "&" + str(avgErrNum2) + "&" + bfText1 + "&" + bfText2 + "&" + bfVar1 + "&" + bfVar2 + "&" + "\\\\ \\hline \n"
outFile.write(text)
outFile.write("\\end{tabular}\n")
#outFile.write("\\end{minipage}\n")
outFile.write("\\end{table}\n")
outFile.write("\\end{center}\n")
outFile.write("\\end{document}\n")
outFile.close()

