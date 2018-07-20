import glob
import os
import commands
import pprint
import sys
import re

#Finds all the vcf files from DV_outputs and then merge them using DV_Merge.sh

dv_outs = glob.glob('DV_outputs/*')

dv_outs.sort()

vcfs = '\''

for folder in dv_outs:
	
	name = folder.replace('DV_outputs/', '')
	vcfs = vcfs + folder + '/' + name + '.vcf.gz '

vcfs = vcfs + '\''
print commands.getoutput('./DV_Merge.sh ' + vcfs)
