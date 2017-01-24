import os
import sys

min_count = 3
fc = 3
min_sample = 5
os.system("~/R-3.3.2/bin/Rscript run_scphaser_cv.R")

for sample_count in range(6, 30, 2):
	for ite in range(0, 10):
	
		os.system("python get_scphaser_vcf_cv.py " + str(sample_count) + " " + str(ite))
		
		print "start scphaser"
		os.system("python scphaser_cv.py " + str(sample_count) + " " + str(ite))
