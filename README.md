# Benchmarking-DeepVariant-against-the-GATK-pipeline
Codes and Scripts for python and bash that automizes the running of DeepVariant and GATK in BIGAS

These scripts and codes are for running GATK and DeepVariant pipeline in BIGAS.

Folder Structure:
Reference_genome: must contain the reference genome with the extension .fa (replace script so it can work on .fasta)
Reads: must contain the read pairs. Filename convention, read pair #1 must have 'R1_001' in the filename and read pair #2 must have 'R2_001' in the filename
Tools: contains picard, gatk3.7 and gatk4.0.5 that is used by the scripts


Codes and Scripts
Main.py: Aligns the reads pairs using Align_Reads.sh, merges the bam files, then calls UnifiedGenotyper_call.sh (creates folder 'UG_outputs' which contains the vcf and its index) and HaplotypeCaller.sh (creates folder 'HC_outputs' which contains the vcf and its index)
  ->Creates the folder 'outputs' which contains: folders per read pair, 'realn_bams' which compiles all the realigned bam files (the actual inputs for UnifiedGenotyper, HaplotypeCaller, and DeepVariant), and the 'outputs_merged.bam' which is the merged bam files from 'realn_bams' folder and it can also be used as inputs for UnifiedGenotyper and HaplotypeCaller.
DV_Main.py: Using the 'real_bams' created by Main.py, it calls the DeepVariant pipeline by calling DeepVariant_call.sh which creates the folder 'DV_outputs' which will contain the bam files folders which has their respective vcfs.
DV_index.py: Finds every vcf files from 'DV_outputs' and index it using tabix
DV_merge.py: Finds and compiles the vcf files from 'DV_outputs' and merge them using DV_Merge.sh which outputs the merged vcfs to the current directory.

Note:
All calls (UnifiedGenotyper, HaplotypeCaller, and DeepVariant, uses the interval file 'sites.intervals'
In running DV_Main.py in BIGAS, the user must be on singularity shell and has already finished aligning the reads using Main.py.


