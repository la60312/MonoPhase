# MonoPhase

## Requirements
* [samtools](http://samtools.sourceforge.net/)
* [ANNOVAR](http://annovar.openbioinformatics.org/en/latest/)

Please add samtools in your $PATH

## Preprocessing
python preproc.py

* --input The directory of input files
* --output The directory for output
* --ref_genome Reference genome file
* --snp_pos SNP position file
* --pair Pair-end = 1; Single-end = 0
* --vcf VCF file

### SNP position file
Contain the chrmosome name and position of SNPs

For example:
chr1    863511
chr1    876200
chr1    883899
chr1    884767
chr1    909419

## Analysis
python analysis.py

* --input The directory of input files
* --output The directory for output
* --snp_info File which contains mapping snp to gene
* --min_count Minimun reads which cover the snp, default: 3
* --min_fc Minimun fold change, default: 3
* --min_sample Minimun count of sample which contain the same imbalanced snp, default: 5

### SNP info file
File which contains mapping snp to gene. It can be generated from ANNOVAR.
For example:
NOC2L   chr1    883899  T       G
PLEKHN1 chr1    909419  C       T
PLEKHN1(uc001acd.3:c.*439C>T,uc001acf.3:c.*439C>T,uc001ace.3:c.*439C>T) chr1    910394  C       T
C1orf170        chr1    914852  G       C
C1orf170        chr1    914940  T       C
C1orf170(uc001ach.2:c.-3T>C)    chr1    916549  A       G
ISG15(uc001acj.4:c.-24_-18del-) chr1    948930  GCCCACA -
ISG15   chr1    949608  G       A
AGRN    chr1    981931  A       G
AGRN    chr1    982994  T       C
AGRN(uc001ack.2:c.*156C>T)      chr1    990517  C       T
AGRN(uc001ack.2:c.*412C>T)      chr1    990773  C       T
AGRN(uc001ack.2:c.*445G>A)      chr1    990806  G       A
AGRN(uc001ack.2:c.*623G>A)      chr1    990984  G       A

###Output file
The output file will be named as *.mono_gene
We generate one output file for each cells, and it contains the monoallelic expressed gene on this cell.
The format is as followed(chr, gene name, position, haplotype, p-value).

chr1,DHDDS,"[26797508, 26797654]",10,01,"[4.51727170970332e-45, 2.29588740394977e-41]"
chr1,C1orf123,"[53679878, 53680090, 53681699]",110,001,"[9.31322574615477e-10, 1.35750788731466e-44, 6.37236764452993e-58]"
chr1,SDCCAG8,"[243468694, 243469029]",11,00,"[1.5407439555098e-33, 2.24207754291969e-44]"
chr1,KIF14,"[200521412, 200522269, 200522351, 200534248]",0000,1111,"[1.50463276905254e-36, 0.015625, 0.0078125, 0.00390625]"
chr1,LAPTM5,"[31205796, 31215364]",00,11,"[2.35098870164461e-38, 5.82076609134676e-11]"

