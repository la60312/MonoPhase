import os
import sys
import random

cmd_type = sys.argv[1]
group_of_sample = list(range(782, 798) + range(802, 814))
sample_num_list = list(range(6, 30, 2))

filter_vcf = "/MMCI/MS/RNAHap/work/vcf_NA12878_giab/NA12878_filter_3.vcf.recode.vcf"
non_filter_vcf = "/MMCI/MS/RNAHap/work/vcf_NA12878_giab/NA12878_chr_het_GT.vcf"
true_vcf = "/MMCI/MS/RNAHap/work/vcf_NA12878_giab/NA12878_chr_het_GTPS.vcf"

for sample_num in sample_num_list:
	for ite in range(0, 10):
		random_samples = random.sample(group_of_sample, sample_num)
		if cmd_type == "combine":
			path = ""
			for i in random_samples:
				path = path + " /MMCI/MS/RNAHap/work/single_cel/SRR764" + str(i) + "/output/mono_phased_qual_5_3_3.vcf" + " /MMCI/MS/RNAHap/work/single_cel/SRR764" + str(i) + "/output/accepted_hits_ID.bam"
			out_dir = '/MMCI/MS/RNAHap/work/single_cel/cv_results/combine_' + str(sample_num)
			
			if not os.path.exists(out_dir):
				os.system('mkdir ' + out_dir)
			os.chdir(out_dir)

			# Phase
			out_file = out_dir + '/tophat_combine_phased.vcf'
			cmd = "whatshap phase --output " + out_file + " " + filter_vcf + path 
			os.system(cmd)

			# Compare			
			cmd = "~/whatshap/venv/bin/whatshap compare --sample NA12878 " + out_file + " " + true_vcf + " > " + out_file + ".compare"
			os.system(cmd)

			# Move all chr file to method_
			cmp_dir = out_dir + '/compare_ite_' + str(ite)

			if not os.path.exists(cmp_dir):
				os.system('mkdir ' + cmp_dir)

			os.system("mv -f chr* " + cmp_dir)

			# Generate csv
			os.system('rm -f ' + out_file)
			os.system('python generate_csv.py ' + out_file + '.compare '  + out_dir + '/ite_' + str(ite) + '.csv')

		elif cmd_type == "exp":
			path = ""
			for i in random_samples:
				path = path + " /MMCI/MS/RNAHap/work/single_cel/SRR764" + str(i) + "/output/mono_phased_qual_5_3_3.vcf"

			out_dir = '/MMCI/MS/RNAHap/work/single_cel/cv_results/exp_' + str(sample_num)
			if not os.path.exists(out_dir):
				os.system('mkdir ' + out_dir)
			os.chdir(out_dir)

			out_file = out_dir + '/tophat_exp_phased.vcf'
			
			# Phase
			cmd = "whatshap phase --output " + out_file + " " + non_filter_vcf  + path 
			os.system(cmd)

			# Compare			
			cmd = "~/whatshap/venv/bin/whatshap compare --sample NA12878 " + out_file + " " + true_vcf + " > " + out_file + ".compare"
			os.system(cmd)

			# Move all chr file to method_
			cmp_dir = out_dir + '/compare_ite_' + str(ite)

			if not os.path.exists(cmp_dir):
				os.system('mkdir ' + cmp_dir)

			os.system("mv -f chr* " + cmp_dir)

			# Generate csv
			os.system('rm -f ' + out_file)
			os.system('python generate_csv.py ' + out_file + '.compare '  + out_dir + '/ite_' + str(ite) + '.csv')
		
		elif cmd_type == "bam":
			path = ""
			for i in random_samples:
				path = path + " /MMCI/MS/RNAHap/work/single_cel/SRR764" + str(i) + "/output/accepted_hits_ID.bam"
			
			out_dir = '/MMCI/MS/RNAHap/work/single_cel/cv_results/bam_' + str(sample_num)

			if not os.path.exists(out_dir):
				os.system('mkdir ' + out_dir)
			os.chdir(out_dir)

			# Phase
			out_file = out_dir + '/tophat_bam_phased.vcf'
			cmd = "whatshap phase --output " + out_file + " " + filter_vcf +  path 
			os.system(cmd)
			
			# Compare			
			cmd = "~/whatshap/venv/bin/whatshap compare --sample NA12878 " + out_file + " " + true_vcf + " > " + out_file + ".compare"
			os.system(cmd)

			# Move all chr file to method_
			cmp_dir = out_dir + '/compare_ite_' + str(ite)

			if not os.path.exists(cmp_dir):
				os.system('mkdir ' + cmp_dir)

			os.system("mv -f chr* " + cmp_dir)

			# Generate csv
			os.system('rm -f ' + out_file)
			os.system('python generate_csv.py ' + out_file + '.compare '  + out_dir + '/ite_' + str(ite) + '.csv')

		
