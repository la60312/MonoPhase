args <- commandArgs(trailingOnly = TRUE)
# Load table
snp = read.table("../annovar/NA12878_chr_het_GTPS.vcf.avinput.hg19_snp138_dropped", sep="\t")
gene = read.table("../annovar/NA12878_pos_info.txt", sep="\t")

refInput = read.table("tophat_total_ref_count.csv", sep = ",")
altInput = read.table("tophat_total_alt_count.csv", sep = ",")

# Remove unused string in gene id
chrIndex = rep("chr", 23)
chrIndex = paste0(chrIndex, c(1:22, "X"))
gene[,1] = sapply(gene[, 1], as.character)
for(i in 1:dim(gene)[1]){
	if(grepl("\\(",gene[i,1])){
		gene[i,1] = strsplit(as.character(gene[i,1]),"\\(")[[1]][1]
	} else{
		gene[i,1] = as.character(gene[i,1])
	}
}

# Map gene id and snp id to all snp
featTable = NULL
refCount = NULL
altCount = NULL
for(i in 1:23){
	snpTmp = snp[snp[,3] == chrIndex[i],]
	geneTmp = gene[gene[,2] == chrIndex[i],]
	inputTmp = refInput[refInput[,1] == chrIndex[i],]
	altInputTmp = altInput[altInput[,1] == chrIndex[i],]
	snpIndex = match(inputTmp[,2], snpTmp[,4])
	naIndex = which(is.na(snpIndex))
	if(length(naIndex) > 0){
		inputTmp = inputTmp[-naIndex,]
		altInputTmp = altInputTmp[-naIndex,]
		snpIndex = snpIndex[-naIndex]
	}
	geneIndex = match(inputTmp[,2], geneTmp[,3])
	naIndex = which(is.na(geneIndex))
	feat = cbind(geneTmp[geneIndex,], snpTmp[snpIndex, 2])
	
	if(length(naIndex) > 0){
		feat = feat[-naIndex,]
	}

	colnames(feat) = c('feat','chr', 'pos', 'ref', 'alt', 'var' )
	featTable = rbind(featTable, feat)
	colnames(featTable) = c('feat','chr', 'pos', 'ref', 'alt', 'var' )
	
	if(length(naIndex) > 0){
		altInputTmp = altInputTmp[-naIndex,]
		inputTmp = inputTmp[-naIndex,]
	}
	rownames(inputTmp) = feat[,6]
	rownames(altInputTmp) = feat[,6]
	ref = inputTmp[,3:30]
	alt = altInputTmp[,3:30]
	refCount = rbind(refCount, ref)
	altCount = rbind(altCount, alt)
}

names = paste0(rep("SRR764", 28), c(782:797, 802:813))
colnames(refCount) = names
colnames(altCount) = names
sample =  as.data.frame(names)
colnames(sample) = "sample"
library(scphaser)
featTable$feat = as.character(featTable$feat)
featTable$ref = as.character(featTable$ref)
featTable$alt = as.character(featTable$alt)
featTable$var = as.character(featTable$var)
refCount = as.matrix(refCount)
altCount = as.matrix(altCount)
rownames(featTable) = featTable$var
rownames(sample) = names


sample_total_list = c(1:28)

for(sample_count in seq(6, 28, by = 2)){
	for(ite in 0:9){
		sample_index = sample(sample_total_list, sample_count)
		# Make acset
		a = as.data.frame(sample[sample_index,])
		rownames(a) = a[,1]
		colnames(a) = c("sample")

		data = new_acset(featdata = featTable, refcount = refCount[,sample_index], altcount = altCount[,sample_index], phenodata = a)
		acset = data
		#acset = filter_homovars(acset, 0.1, 0.1)
		acset = call_gt(acset, 3, 3)
		acset = filter_acset(acset, 5)
		
		type = c('ac', 'gt')
		weight = c(TRUE, FALSE)
		method = c('exaust', 'pam')
		chr = paste0(rep("chr", 22), c(1:22))
		chr = c(chr, "chrX")
		
		methodIndex = 1
		typeIndex = 1
		weightIndex = 2

		acset = phase(acset, input = type[typeIndex], weigh = weight[weightIndex], method = method[methodIndex]	)
	
		refAll = c()
		altAll = c()
		dataAll = c()
		
		for(i in c(1:23)){
		        index = which(acset$featdata[, 2] == chr[i])
		        data = acset$featdata[index,]
		        refData = acset$refcount[index,]
		        altData = acset$altcount[index,]
		        index = order(data[, 3])
		        data = data[index, c(2, 3, 1, 6)]
		        refData = refData[index,]
		        altData = altData[index,]
		        dataAll = rbind(dataAll, data)
		        refAll = rbind(refAll, refData)
		        altAll = rbind(altAll, altData)
		}
		phasedData = acset$phasedfeat[rownames(dataAll),]
		phasedData = cbind(dataAll[, 1:2], phasedData)
		hap1 = as.integer(phasedData[, 'hapA'] ==  phasedData[, 'ref'])
		hap2 = as.integer(phasedData[, 'hapB'] ==  phasedData[, 'ref'])
		phasedData = cbind(phasedData, paste0(hap1, "|", hap2))
			fileName = paste0("tophat_scphaser_cv/scphaser_tophat_", sample_count,'_',ite, ".csv")
		write.table(phasedData, file = fileName, sep="\t", col.names = F, row.names = F)
	}
}
