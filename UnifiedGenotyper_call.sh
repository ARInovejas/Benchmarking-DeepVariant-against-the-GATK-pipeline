#!/bin/bash

bam_files=$1

rm -R UG_outputs
mkdir UG_outputs

module load jdk
#Call UnifiedGenotyper given the refenrece IRGSP-1.0_genome.fa and the input bam files
java -Xmx8g -jar Tools/gatk3.7/GenomeAnalysisTK.jar \
	-T UnifiedGenotyper \
	-I $bam_files \
	-R Reference_genome/IRGSP-1.0_genome.fa \
	-o UG_outputs/UnifiedGenotyper_output.vcf \
	-L sites.intervals

module load htslib
bgzip UG_outputs/UnifiedGenotyper_output.vcf
tabix UG_outputs/UnifiedGenotyper_output.vcf.gz
