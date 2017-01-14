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
			os.system("~/R-3.3.2/bin/Rscript run_scphaser.R " + cmd_type)

			os.system("python get_scphaser_vcf.py " + str(min_count) + " " + str(fc) + " " + str(min_sample) + " " + cmd_type)
			
			print "start scphaser"
			os.system("python scphaser.py "  + str(min_count) + " " + str(fc) + " " + str(min_sample) + " " + cmd_type)
