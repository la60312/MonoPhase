import os
import sys


path = ""
sample_count = sys.argv[1]
ite = sys.argv[2]

prefix = "/MMCI/MS/RNAHap/work/single_cel/tophat_scphaser_cv/scphaser_tophat_"


input_type = ['ac', 'gt']
weight = ['TRUE', 'FALSE']
method = ['exaust', 'pam']

# For loop to run all 8 settings
method_index = 0
type_index = 0
weight_index = 1
input_file = prefix + sample_count + "_" + ite + ".vcf"
out_dir = '/MMCI/MS/RNAHap/work/single_cel/cv_results/scphaser_' + sample_count

if not os.path.exists(out_dir):
	os.system('mkdir ' + out_dir)
os.chdir(out_dir)

out_file = out_dir + "/scphaser_" + ite + ".vcf"
cmd = "~/whatshap/venv/bin/whatshap compare --sample NA12878 " + input_file + " /MMCI/MS/RNAHap/work/vcf_NA12878_giab/NA12878_chr_het_GTPS.vcf > " + out_file + ".compare"
os.system(cmd)

# Move all chr file to method_
cmp_dir = out_dir + '/compare_ite_' + ite

if not os.path.exists(cmp_dir):
	os.system('mkdir ' + cmp_dir)

os.system("mv -f chr* " + cmp_dir)

# Generate csv
os.system('rm -f ' + out_file)
os.system('python generate_csv.py ' + out_file + '.compare '  + out_dir + '/ite_' + ite + '.csv')


