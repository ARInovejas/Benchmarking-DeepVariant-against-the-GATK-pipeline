import glob
import os
import commands
import pprint
import sys
import re


ref = glob.glob('Reference_genome/*.fa') #gets the reference genome
read1s = glob.glob('Reads/*R1_001*') #gets all the 1st reads
read2s = glob.glob('Reads/*R2_001*') #gets all the 2nd reads
#sort them so the pairs will be aligned to each other
read1s.sort()
read2s.sort()

#bash script that aligns the read pairs
alignScript = './Align_Reads.sh '
#default output directory for each alignment
outputDir = 'outputs/'
#final output directory for .realn.bam (the files that would be merged)
outputRealn = 'outputs/realn_bams'

#create necessary folders
commands.getoutput('rm -R outputs')
commands.getoutput('mkdir outputs')
commands.getoutput('mkdir ' + outputRealn)

#gets the bam files' paths
bam_files = ''

#number of read pairs
N = len(read1s)

for i in range(0,N):

	#gets the read's name from the dataset
	readName = re.sub('Reads/', '', read1s[i])
	readName = re.sub('_R1_001.fastq.gz', '', readName)
	
	print "Aligning " + readName
	#Call align Script. Pass the necessary parameters
	commands.getoutput(alignScript + ref[0].replace('.fa', '') + ' ' + read1s[i] + ' ' + read2s[i] + ' ' + (outputDir + readName) + ' ' + outputRealn + ' ' + readName)
	#final output is the (Read-Pair-Name).realn.bam to the folder outputs/realn_bams

	print "Finished Aligning " + readName

	bam_files = bam_files + 'outputs/realn_bams/' + readName + '.realn.bam \\'
	if i!=(N-1):
		bam_files = bam_files + 'I='

#Merge bam files
print "Merging Bam Files"
commands.getoutput('module load picard && picard MergeSamFiles \\I=' + bam_files + 'O=outputs/outputs_merged.bam')
commands.getoutput('module load samtools && samtools index outputs/outputs_merged.bam')
print "Finished Merging Bam Files"

#Call Unified Genotyper
print "Calling UnifiedGenotyper..."
commands.getoutput('./UnifiedGenotyper_call.sh outputs/outputs_merged.bam')
print "Finished Calling UnifiedGenotyper"
#Call Haplotype Caller
print "Calling HaplotypeCaller...."
commands.getoutput('./HaplotypeCaller_call.sh outputs/outputs_merged.bam')
print "Finished Calling HaplotypeCaller"
