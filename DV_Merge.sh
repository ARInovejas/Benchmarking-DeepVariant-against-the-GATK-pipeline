#!/bin/bash

module load vcftools
module load htslib

VCFS=$1

#Merges the given VCF files
echo $VCFS
vcf-merge $VCFS | bgzip -c > DeepVariant_output.vcf.gz
