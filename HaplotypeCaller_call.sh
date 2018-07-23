#!/bin/bash

bam_files=$1

rm -R HC_outputs
mkdir HC_outputs

module load gatk/4.0.5.2
#Call HaplotypeCaller given the refenrece IRGSP-1.0_genome.fa and the input bam files
gatk HaplotypeCaller  \
   -R Reference_genome/IRGSP-1.0_genome.fa \
   -I $bam_files \
   -O HC_outputs/HaplotypeCaller_output.vcf \
   -L sites.intervals

module load htslib
bgzip HC_outputs/HaplotypeCaller_output.vcf
tabix HC_outputs/HaplotypeCaller_output.vcf.gz
