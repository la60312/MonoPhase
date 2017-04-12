import os
import vcf
import csv
import sys
from os import listdir
from os.path import isfile, join
import argparse

parser = argparse.ArgumentParser(description='Preprocessing')
parser.add_argument('--input', dest='input_dir', help='input file dir', required=True)
parser.add_argument('--output', dest='out_dir', help='output file dir', required=True)
parser.add_argument('--ref_genome', dest='ref_genome', help='Reference genome', required=True)
parser.add_argument('--snp_pos', dest='snp_pos', help='Snp position file', required=True)
parser.add_argument('--pair', dest='pair_end', help='Pair end = 1, Single end = 0', required=True)
parser.add_argument('--vcf', dest='vcf_file', help='VCF file', required=True)

args = parser.parse_args()

input_dir = args.input_dir
out_dir = args.out_dir
ref_genome = args.ref_genome
snp_pos = args.snp_pos
pair_end = args.pair
vcf_file = args.vcf_file


input_file_list = [f for f in listdir(input_dir) if isfile(join(input_dir, f))]
input_file_list = [fi for fi in input_file_list if fi.endswith(".bam")]

for input_file in input_file_list:
	out_file = out_dir + '/' + '.'.join(input_file.split('.')[:-1]) + ".pileup"
	
	# Run pileup
	if pair_end == '1':
		cmd = "samtools mpileup -A -l " + snp_pos + " -f " + ref_genome + " -Q 30 -q 20 --output " + out_file + " " + input_dir + '/' + input_file
	else:
		cmd = "samtools mpileup -l " + snp_pos + " -f " + ref_genome + " -Q 30 -q 20 --output " + out_file + " " + input_dir + '/' + input_file
	os.system(cmd)
	
	# parse pileup
	cmd = "python parse_pileup.py " + out_file
	os.system(cmd)
	
# Get snp count
cmd = "python get_snp_from_pileup.py " + out_dir + " " + vcf_file
os.system(cmd)
