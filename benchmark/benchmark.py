
def get_vcf_contents(filename): #Get the contents of the given vcf filename
	f = open(filename, 'r')
	contents = []

	for line in f:
		line = line[:-1] #removes new line at the end
		contents.append(line.split('\t'))

	f.close()

	#final output is a 2 dimensional array where
	#rows = taxas
	#columns = sites
	return contents

def get_ref_or_alt(filename, type):
	#type can be either 'ref' or 'alt'

	f = open(filename, 'r')
	ref_alt = []

	if type == 'ref':
		index = 5
	elif type == 'alt':
		index = 6
	else:
		print 'Invalid argument'
		return []
	for line in f:
		line = line.split('\t')
		ref_alt.append(line[index])
	f.close()

	#final output is an array of ref/alt of the given file
	return ref_alt

def get_statistics(vcf1, vcf2, name1, name2):
	
	ref_ref = 0
	alt_alt = 0
	het_het = 0
	unk_unk = 0

	#vcf1 outputs
	ref_to_alt = 0
	ref_to_het = 0
	alt_to_het = 0
	unk_to_ref = 0
	unk_to_alt = 0
	unk_to_het = 0

	#vcf2 outputs
	alt_to_ref = 0
	het_to_ref = 0
	het_to_alt = 0
	ref_to_unk = 0
	alt_to_unk = 0
	het_to_unk = 0

	sites = {}
	if len(vcf1[0]) > len(vcf2[0]):
		#swaps so the lesser site length will be vcf1 (to ensure only intersecting sites will be recorded)
		temp = vcf1
		vcf1 = vcf2
		vcf2 = temp
		temp = name1
		name1 = name2
		name2 = temp

	REF = get_ref_or_alt(name1+'_site_summary.txt', 'ref')
	ALT = get_ref_or_alt(name1+'_site_summary.txt', 'alt')


	for i in range(1, len(vcf2[0])):
		sites[vcf2[0][i]] = i

	for i in range(1, len(vcf1)):
		for j in range(1, len(vcf1[i])):
			if vcf1[0][j] in sites:
				vcf2_genome = vcf2[i][sites[vcf1[0][j]]]
			else:
				continue
			vcf1_genome = vcf1[i][j]

			if vcf1_genome == vcf2_genome: #same results
				if vcf1_genome == REF[j]:
					ref_ref = ref_ref + 1
				elif vcf1_genome == ALT[j]:
					alt_alt = alt_alt + 1
				elif vcf1_genome in HETS:
					het_het = het_het + 1
				elif vcf1_genome == UNK:
					unk_unk = unk_unk + 1


			elif vcf1_genome == REF[j] and vcf2_genome == ALT[j]: #Ref-Alt vcf1
				ref_to_alt = ref_to_alt + 1

			elif vcf1_genome == REF[j] and vcf2_genome in HETS: #Ref-Het vcf1
				ref_to_alt = ref_to_het + 1

			elif vcf1_genome == ALT[j] and vcf2_genome in HETS: #Alt-Het vcf1
				alt_to_het = alt_to_het + 1

			elif vcf1_genome == ALT[j] and vcf2_genome == REF[j]: #Ref-Alt vcf2
				alt_to_ref = alt_to_ref + 1

			elif vcf1_genome in HETS and vcf2_genome == REF[j]: #Ref-Het vcf2
				het_to_ref = het_to_ref + 1

			elif vcf1_genome in HETS and vcf2_genome == ALT[j]: #Alt-Het vcf2
				het_to_alt = het_to_alt + 1

			elif vcf1_genome == UNK and vcf2_genome == REF[j]: #Unk-Ref vcf1
				unk_to_ref = unk_to_ref + 1

			elif vcf1_genome == UNK and vcf2_genome == ALT[j]: #Unk-Alt vcf1
				unk_to_alt = unk_to_alt + 1

			elif vcf1_genome == UNK and vcf2_genome in HETS: #Unk-Het vcf1
				unk_to_het = unk_to_het + 1

			elif vcf1_genome == REF[j] and vcf2_genome == UNK: #Unk-Ref vcf2
				ref_to_unk = ref_to_unk + 1

			elif vcf1_genome == ALT[j] and vcf2_genome == UNK: #Unk-Alt vcf2
				alt_to_unk = alt_to_unk + 1

			elif vcf1_genome in HETS and vcf2_genome == UNK: #Unk-Het vcf2
				alt_to_unk = ref_to_unk + 1



	print
	print "Column: " + name1
	print "Row: " + name2
	print '\tREF\tALT\tHET\tUNK'
	print 'REF\t' + str(ref_ref) + '\t' + str(alt_to_ref) + '\t' + str(het_to_ref) + '\t' + str(unk_to_ref)
	print 'ALT\t' + str(ref_to_alt) + '\t' + str(alt_alt) + '\t' + str(het_to_alt) + '\t' + str(unk_to_alt)
	print 'HET\t' + str(ref_to_het) + '\t' + str(alt_to_het) + '\t' + str(het_het) + '\t' + str(unk_to_het)
	print 'UNK\t' + str(ref_to_unk) + '\t' + str(alt_to_unk) + '\t' + str(het_to_unk) + '\t' + str(unk_unk)
	print

	f = open('Statistics',  'a')

	f.write("Column: " + name1 + '\n')
	f.write("Row: " + name2 + '\n')
	f.write('\tREF\tALT\tHET\tUNK' + '\n')
	f.write('REF\t' + str(ref_ref) + '\t' + str(alt_to_ref) + '\t' + str(het_to_ref) + '\t' + str(unk_to_ref) + '\n')
	f.write('ALT\t' + str(ref_to_alt) + '\t' + str(alt_alt) + '\t' + str(het_to_alt) + '\t' + str(unk_to_alt) + '\n')
	f.write('HET\t' + str(ref_to_het) + '\t' + str(alt_to_het) + '\t' + str(het_het) + '\t' + str(unk_to_het) + '\n')
	f.write('UNK\t' + str(ref_to_unk) + '\t' + str(alt_to_unk) + '\t' + str(het_to_unk) + '\t' + str(unk_unk) + '\n')
	f.write('\n')
	f.close()




#VCFS
UG = get_vcf_contents('UnifiedGenotyper_vcf.txt')
HC = get_vcf_contents('HaplotypeCaller_vcf.txt')
DV = get_vcf_contents('DeepVariant_vcf.txt')

#Constants
HETS = ['R', 'Y', 'S', 'W', 'K', 'M']
UNK = 'N'


#Number of Sites
UG_site_num = len(UG[0]) - 1
HC_site_num = len(HC[0]) - 1
DV_site_num = len(DV[0]) - 1
sites_stats = 'UnifiedGenotyper: ' + str(UG_site_num) + '\nHaplotypeCaller: ' + str(HC_site_num) + '\nDeepVariant: ' + str(DV_site_num) + '\n'

#creates/clears file Statistics
f = open('Statistics', 'w+')
f.write('Number of Sites\n' + sites_stats + '\n')
f.close()

print 'Number of Sites'
print sites_stats

#Get Statistics
get_statistics(HC, UG, 'HaplotypeCaller', 'UnifiedGenotyper')
get_statistics(HC, DV, 'HaplotypeCaller', 'DeepVariant')
get_statistics(DV, UG, 'DeepVariant', 'UnifiedGenotyper')
