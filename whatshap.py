import os
import sys


cmd_type = sys.argv[1]
if cmd_type == 'exp':
	min_count = sys.argv[2]
	fc = sys.argv[3]
	min_sample = sys.argv[4]
	src_type = sys.argv[5]



if cmd_type == "combine":
	path = ""
	for i in range(782, 798) + range(802, 814):
		path = path + " /MMCI/MS/RNAHap/work/single_cel/SRR764" + str(i) + "/output/mono_phased_qual_5_3_3.vcf" + " /MMCI/MS/RNAHap/work/single_cel/SRR764" + str(i) + "/output/accepted_hits_ID.bam"
	
	out_file = 'results/tophat_combine_phased_5.vcf'
	cmd = "whatshap phase --output " + out_file + " ../vcf_NA12878_giab/NA12878_filter_5.vcf.recode.vcf" +  path 
	os.system(cmd)
	
	cmd = "~/whatshap/venv/bin/whatshap compare --sample NA12878 " + out_file + " ../vcf_NA12878_giab/NA12878_chr_het_GTPS.vcf > " + out_file + ".compare"
	os.system(cmd)
	#if src_type == "star":	
		#out_dir = "results/wh_sc_data_" + min_sample + "_" + min_count + "_" + fc + "_log"
	
#	out_dir = "star_whatshap_filter/wh_" + min_sample + "_" + min_count + "_" + fc + "_log"
#	else:
		#out_dir = "results/wh_" + min_sample + "_" + min_count + "_" + fc + "_log"
	out_dir = "results/tophat_combine_5_log/"
	os.system("mkdir " + out_dir)
	os.system("mv chr* " + out_dir)

elif cmd_type == "exp":
	path = ""
	for i in range(782, 798) + range(802, 814):
		if src_type == "star":
			path = path + " /MMCI/MS/RNAHap/work/single_cel/SRR764" + str(i) + "/star_output/mono_phased_" + min_sample + "_" + min_count + "_" + fc + ".vcf"
			#path = path + " /MMCI/MS/RNAHap/work/single_cel/SRR764" + str(i) + "/star_output/mono_phased_sc_" + min_sample + "_" + min_count + "_" + fc + ".vcf"
		else:
			path = path + " /MMCI/MS/RNAHap/work/single_cel/SRR764" + str(i) + "/output/mono_phased_qual_" + min_sample + "_" + min_count + "_" + fc + ".vcf"
	
	if src_type == "star":
		out_file = "star_whatshap_filter/wh_" + min_sample + "_" + min_count + "_" + fc + ".vcf"
		#cmd = "whatshap phase --output " + out_file + " sc_data.vcf" +  path 
		cmd = "whatshap phase --output " + out_file + " ../vcf_NA12878_giab/NA12878_chr_het_GT.vcf" +  path 
	else:
		#out_file = "results/wh_" + min_sample + "_" + min_count + "_" + fc + ".vcf"
		out_file = "tophat_whatshap_filter_qual/wh_" + min_sample + "_" + min_count + "_" + fc + ".vcf"
		cmd = "whatshap phase --output " + out_file + " ../vcf_NA12878_giab/NA12878_chr_het_GT.vcf" +  path 

	os.system(cmd)
	
	cmd = "whatshap compare --sample NA12878 " + out_file + " ../vcf_NA12878_giab/NA12878_chr_het_GTPS.vcf > " + out_file + ".compare"
	os.system(cmd)
	if src_type == "star":	
		#out_dir = "results/wh_sc_data_" + min_sample + "_" + min_count + "_" + fc + "_log"
		out_dir = "star_whatshap_filter/wh_" + min_sample + "_" + min_count + "_" + fc + "_log"
	else:
		#out_dir = "results/wh_" + min_sample + "_" + min_count + "_" + fc + "_log"
		out_dir = "tophat_whatshap_filter_qual/wh_" + min_sample + "_" + min_count + "_" + fc + "_log"
	os.system("mkdir " + out_dir)
	os.system("mv chr* " + out_dir)

elif cmd_type == "bam":
	path = ""
	for i in range(782, 798) + range(802, 814):
		path = path + " /MMCI/MS/RNAHap/work/single_cel/SRR764" + str(i) + "/star_output/Aligned.sortedByCoord_ID.out.bam"
		#path = path + " /MMCI/MS/RNAHap/work/single_cel/SRR764" + str(i) + "/output/accepted_hits_ID.bam"
	
	#out_file = 'results/bam_tophat_phased_filter_3.vcf'
	out_file = 'results/bam_star_phased_filter_10.vcf'
	cmd = "whatshap phase --output " + out_file + " ../vcf_NA12878_giab/NA12878_star_filter_10.vcf.recode.vcf" +  path 
	os.system(cmd)
	
	cmd = "whatshap compare " + out_file + " ../vcf_NA12878_giab/NA12878_chr_het_GTPS.vcf > " + out_file + ".compare"
	os.system(cmd)

elif cmd_type == "exp_log":
	path = ""
	for i in range(782, 798) + range(802, 814):
		path = path + " /MMCI/MS/RNAHap/work/single_cel/SRR764" + str(i) + "/output/mono_all_chr_phased.vcf"
	
	out_file = 'results/exp_log_phased.vcf'
	cmd = "whatshap phase --output " + out_file + " ../vcf_NA12878_giab/NA12878_chr_het_GTPS.vcf" +  path 
	os.system(cmd)
	
	cmd = "~/whatshap/venv/bin/whatshap compare --sample NA12878 " + out_file + " ../vcf_NA12878_giab/NA12878_chr_het_GTPS.vcf > " + out_file + ".compare"
	os.system(cmd)
	os.system("mv chr* results/exp_log")





