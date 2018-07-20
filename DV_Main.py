import glob
import os
import commands
import pprint
import sys
import re

#must be on the singularity shell before running

intervals = ''

#reads the sites.intervals and converts it to a single line string
f = open('sites.intervals', 'r')

for line in f:
	intervals = intervals + line.replace('\n', ' ')

f.close()

commands.getoutput('rm -R DV_outputs && mkdir DV_outputs')

#gets the bam files to input on DeepVariant_call.sh
ref = 'Reference_genome/IRGSP-1.0_genome.fa'

reads.sort()

for bam in reads:
	
	name = bam.replace('outputs/realn_bams/', '')
	name = name.replace('.realn.bam', '')
	
	print commands.getoutput('./DeepVariant_call.sh ' + ref + ' ' + bam + ' ' + name + ' \'' + intervals + '\'')

