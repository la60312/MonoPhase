args <- commandArgs(trailingOnly = TRUE)

input_name = args[1]
output = args[2]
min_count = as.integer(args[3])
fc = as.integer(args[4])

fc_up = fc
fc_low = 1 / fc

data = read.table(input_name, sep = ",")

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
data = data[data[, 7] < 0.05,]
data = data[order(data[,1]),]
name_list = strsplit(input_name, "[.]")[[1]]
input_name = paste(name_list[-length(name_list)], collapse=".")
input_name = paste0(input_name, ".binomial")
name_list = strsplit(input_name, "[/]")[[1]]
fileName = paste0(output, "/", name_list[length(name_list)])
write.table(data, file = fileName)
