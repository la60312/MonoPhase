import os
import sys


path = ""
sample_count = sys.argv[1]
ite = sys.argv[2]

prefix = "tophat_scphaser_cv/scphaser_tophat_"


input_type = ['ac', 'gt']
weight = ['TRUE', 'FALSE']
method = ['exaust', 'pam']

# For loop to run all 8 settings
method_index = 0
type_index = 0
weight_index = 1
input_file = prefix + sample_count + "_" + ite + ".vcf"
out_file = prefix + sample_count + "_" + ite + ".vcf"

cmd = "whatshap compare --sample NA12878 " + input_file + " ../vcf_NA12878_giab/NA12878_chr_het_GTPS.vcf > " + out_file + ".compare"
os.system(cmd)

ite_file = prefix + sample_count + "_" + ite + "_ite.csv" 
os.system('python generate_csv.py ' + out_file + '.compare ' +  ite_file)


