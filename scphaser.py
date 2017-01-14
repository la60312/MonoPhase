import os
import sys


path = ""
min_count = sys.argv[1]
fc = sys.argv[2]
min_sample = sys.argv[3]
data_src = sys.argv[4]

if data_src == "star":
	prefix = "star_scphaser/scphaser_star_"
else:
	prefix = "tophat_scphaser/scphaser_tophat_"


input_type = ['ac', 'gt']
weight = ['TRUE', 'FALSE']
method = ['exaust', 'pam']

# For loop to run all 8 settings
for method_index in range(0, 2):
	for type_index in range(0, 2):
		for weight_index in range(0, 2):
			input_file = prefix + method[method_index] + "_" + input_type[type_index] + "_" + weight[weight_index] + "_" + min_sample + "_" + min_count + "_" + fc + ".vcf"
			out_file = prefix + method[method_index] + "_" + input_type[type_index] + "_" + weight[weight_index] + "_" + min_sample + "_" + min_count + "_" + fc + ".vcf"

			cmd = "~/whatshap/venv/bin/whatshap compare --sample NA12878 " + input_file + " ../vcf_NA12878_giab/NA12878_chr_het_GTPS.vcf > " + out_file + ".compare"
			#cmd = "~/whatshap/venv/bin/whatshap compare --sample NA12878 " + input_file + " sc_data.vcf > " + out_file + ".compare"
			os.system(cmd)
			out_dir = prefix + method[method_index] + "_" + input_type[type_index] + "_" + weight[weight_index] + "_" + min_sample + "_" + min_count + "_" + fc + "_log"
			os.system("mkdir " + out_dir)
			os.system("mv chr* " + out_dir)


