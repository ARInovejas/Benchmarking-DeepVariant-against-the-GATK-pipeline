#!/bin/bash

MODEL="/home/models/model.ckpt"

REF=$1 #reference
BAM=$2 #aligned bam file
RDName=$3 #read name
INTERVALS=$4 #intervals as a string

mkdir DV_outputs/${RDName}


python /home/bin/make_examples.zip \
  --mode calling   \
  --ref "${REF}"   \
  --reads "${BAM}" \
  --examples DV_outputs/${RDName}/${RDName}.tfrecord.gz \
  --sample_name "${RDName}" \
  --regions "${INTERVALS}"

# --regions "intervals as strings separated by space"
# --regions "chr01:10000-11000 chr01:13000-20000 ...."

python /home/bin/call_variants.zip \
 --outfile DV_outputs/${RDName}/call_variants_output.vcf.gz \
 --examples DV_outputs/${RDName}/${RDName}.tfrecord.gz \
 --checkpoint "${MODEL}"

python /home/bin/postprocess_variants.zip \
  --ref "${REF}" \
  --infile DV_outputs/${RDName}/call_variants_output.vcf.gz \
  --outfile DV_outputs/${RDName}/${RDName}.vcf.gz
