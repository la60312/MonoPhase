import os
import vcf
import csv
import sys
from os import listdir
from os.path import isfile, join
import argparse

parser = argparse.ArgumentParser(description='Analysis')
parser.add_argument('--input', dest='input_dir', help='input file dir', required=True)
parser.add_argument('--output', dest='out_dir', help='output file dir', required=True)
parser.add_argument('--snp_info', dest='snp_info', help='File which contains mapping snp to gene', required=True)
parser.add_argument('--min_count', dest='min_count', help='Minimun reads which cover the snp', default="3")
parser.add_argument('--min_fc', dest='min_fc', help='Minimun fold change', default="3")
parser.add_argument('--min_sample', dest='min_sample', help='Minimun count of sample which contain the same imbalanced snp', default="5")

args = parser.parse_args()

input_dir = args.input_dir
out_dir = args.out_dir
snp_info = args.snp_info
min_count = args.min_count
fc = args.min_fc
min_sample = args.min_sample

print "min read count: " + min_count
print "min fold change: " + fc
print "min sample number: " + min_sample


input_file_list = [f for f in listdir(input_dir) if isfile(join(input_dir, f))]
input_file_list = [fi for fi in input_file_list if fi.endswith(".snp_count.csv")]

for input_file in input_file_list:
	input_file = input_dir + '/' + input_file
	os.system("Rscript binomial.R " + input_file + " " + out_dir + " " + min_count + " " + fc)

print "binomial test complete"

print "intersect with ucsc gene then save all mono gene into mono_gene.csv"
os.system("python gene_isec.py " + out_dir + " " + snp_info + " " + min_count + " " + fc + " " + min_sample)

