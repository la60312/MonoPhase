import os

for i in range(785, 798) + range(802, 814):
	path = "/MMCI/MS/RNAHap/work/single_cel/SRR764" + str(i) + "/output/"
	os.chdir(path)

        #cmd = "samtools mpileup -l ../../../vcf_NA12878_giab/NA12878_chr_het_pos.txt -f ../../../refGenome/hg19.fa -Q 20 --output pileup_all_pos Aligned.sortedByCoord_ID.out.bam"
        cmd = "samtools mpileup -l ../../../vcf_NA12878_giab/NA12878_pos.txt -f ../../../refGenome/hg19.fa -Q 30 -q 20 --output pileup accepted_hits_ID.bam"
        os.system(cmd)
