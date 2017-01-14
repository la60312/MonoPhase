args <- commandArgs(trailingOnly = TRUE)

name = paste0(rep("SRR764", 28), c(782:797, 802:813))

min_count = as.integer(args[1])
fc = as.integer(args[2])
data_type = args[3]

fc_up = fc
fc_low = 1 / fc

for(sample_index in 1:28){
	if(data_type == "star"){
		#input_name = paste0(name[sample_index], "/star_output/.csv") 
		input_name = paste0(name[sample_index], "/star_output/snp_info_star_30.csv") 
	}
	else{
		input_name = paste0(name[sample_index], "/output/snp_info_tophat_30.csv") 
		#input_name = paste0(name[sample_index], "/star_output/snp_info_star_30.csv") 
	}
	data = read.table(input_name, sep = ",")
	
	#count_index = which(data[, 4] + data[, 5] > 10)
	count_index = which(rowSums(data[,c(4, 5)] >= min_count) >= 1)
	data = data[count_index,]
	for(i in c(1: length(data[,2]))){
		data[i, 7] = binom.test(c(data[i, 4], data[i, 5]), 5/10, alternative="two.sided")$p.value
	}
	threshold_up = 0.00000000001 * fc 	
	threshold_low = 0.00000000001 	
	index_low = which(((data[,4] + threshold_low) / (data[,5] + threshold_up)) <= fc_low)
	index_up = which(((data[,4] + threshold_up) / (data[,5] + threshold_low)) >= fc_up)
	index = sort(c(index_low, index_up))
	data = data[index,]
	
	
	data_fail = data[data[,7] >= 0.05,]
	#data_fail = data_fail[order(data_fail[,1]),]
	data = data[data[, 7] < 0.05,]
	data = data[order(data[,1]),]
	if(data_type == "star"){
		#fileName = paste0(name[sample_index], "/star_output/binomial_snp_sc", "_", args[1], "_", args[2] ,".csv")
		fileName = paste0(name[sample_index], "/star_output/binomial_snp", "_", args[1], "_", args[2],".csv")
	}
	else{
		fileName = paste0(name[sample_index], "/output/binomial_snp", "_", args[1], "_", args[2],".csv")
		#fileName = paste0(name[sample_index], "/star_output/binomial_snp", "_", args[1], "_", args[2],".csv")
	}
	write.table(data, file = fileName)
	
	#fileName = paste0(args[1], "/star_output/binomial_snp_fail_30.csv")
	#write.table(data_fail, file = fileName)
}
