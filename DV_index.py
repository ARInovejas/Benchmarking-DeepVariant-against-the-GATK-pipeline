import glob
import os
import commands
import pprint
import sys
import re

#Finds all the vcf files from DV_outputs and index it

dv_outs = glob.glob('DV_outputs/*')

dv_outs.sort()

for folder in dv_outs:
	
	name = folder.replace('DV_outputs/', '')
	print commands.getoutput('module load htslib && tabix ' + folder + '/' + name + '.vcf.gz')
