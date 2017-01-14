import os

for i in range(782, 784):
	path = "/MMCI/MS/RNAHap/work/single_cel/SRR764" + str(i) + "/output/"
	os.chdir(path)
	
	cmd = "freebayes --min-mapping-quality 20 --haplotype-length 0 --report-monomorphic --min-base-quality 20 --min-alternate-count 0 --min-alternate-fraction 0 --pooled-continuous -l -f ../../../refGenome/hg19.fa -@ ../../../vcf_NA12878_giab/NA12878_exon.vcf.gz accepted_hits_ID.bam > variant_exon.vcf"
	#cmd = "freebayes --min-mapping-quality 20 --haplotype-length 0 --report-monomorphic --min-base-quality 20 --min-alternate-count 0 --min-alternate-fraction 0 -f ../../../refGenome/hg19.fa accepted_hits_ID_sort.bam > variant_test.vcf"
	os.system(cmd)

        cmd = "rm -rf " + path + "isec"
        #os.system(cmd)
        cmd = "cp " + path + "variant_exon.vcf " + path + "variant_exon_back.vcf"
        os.system(cmd)

        cmd = "bgzip -c " + path + "variant_exon.vcf > " + path + "variant_exon.vcf.gz"
        os.system(cmd)
        cmd = "tabix -p vcf " + path + "variant_exon.vcf.gz"
        os.system(cmd)
        cmd = "bcftools isec -p " + path + "isec " + path + "variant_exon.vcf.gz ../../../vcf_NA12878_giab/NA12878_exon.vcf.gz"
        os.system(cmd)
        cmd = "cp " + path + "variant_exon_isec.vcf " + path + "variant_exon_isec_back.vcf"
        os.system(cmd)
        cmd = "cp " + path + "isec/0002.vcf " + path + "variant_exon_isec.vcf"
        os.system(cmd)

        cmd = "rm -rf " + path + "isec"
        #os.system(cmd)
