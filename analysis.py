import os
import sys

for min_count in range(3, 11):
	for fc in range(3, 4):
		for min_sample in range(5, 6):
			cmd_type = sys.argv[1]
			
			print "min read count: " + str(min_count)
			print "min fold change: " + str(fc)
			print "min sample number: " + str(min_sample)
			print "data type: " + cmd_type
			
			os.system("Rscript binomial.R " + str(min_count) + " " + str(fc) + " " + cmd_type)
			
			print "binomial test complete"
			
			print "intersect with ucsc gene then save all mono gene into mono_gene.csv"
			os.system("python gene_isec.py " + str(min_count) + " " + str(fc) + " " + str(min_sample) + " " + cmd_type)
			
			print "start to output phased vcf"
			os.system("python get_phased_vcf.py " + str(min_count) + " " + str(fc) + " " + str(min_sample) + " " + cmd_type)
			
			print "start whatshap"
			os.system("python whatshap.py exp "  + str(min_count) + " " + str(fc) + " " + str(min_sample) + " " + cmd_type)
