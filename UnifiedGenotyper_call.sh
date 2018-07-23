#!/bin/bash

bam_files=$1

rm -R UG_outputs
mkdir UG_outputs

module load gatk/3.7
#Call UnifiedGenotyper given the refenrece IRGSP-1.0_genome.fa and the input bam files
gatk \
	-T UnifiedGenotyper \
	-I $bam_files \
	-R Reference_genome/IRGSP-1.0_genome.fa \
	-o UG_outputs/UnifiedGenotyper_output.vcf \
	-L sites.intervals

module load htslib
bgzip UG_outputs/UnifiedGenotyper_output.vcf
tabix UG_outputs/UnifiedGenotyper_output.vcf.gz
