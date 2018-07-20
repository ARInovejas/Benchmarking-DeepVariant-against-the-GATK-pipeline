#!/bin/bash

module load bwa
module load samtools
module load jdk

REF=$1 #arg 1, reference
RD1=$2 #arg 2, 1st read pair
RD2=$3 #arg 3, 2nd read pair
OUT=$4/$6 #arg4, output folder
OUTrealn=$5 #arg5, final outputs folder (.realn.bam) for merging
RDName=$6 #arg 6, read name
PICARD=Tools/picard/picard.jar #path for picard.jar
GATK=Tools/gatk3.7/GenomeAnalysisTK.jar #path for gatk jar to be used


#create output folder
mkdir $4 

#ALIGNMENT

#Index Reference for Alignment
bwa index $REF.fa

#Align
bwa mem -M -t 8 $REF.fa $RD1 $RD2 > $OUT.sam

#SortSam
java -Xmx8g -jar $PICARD SortSam \
	INPUT=$OUT.sam \
	OUTPUT=$OUT.sorted.bam \
	SO=coordinate \
	VALIDATION_STRINGENCY=LENIENT \
	CREATE_INDEX=TRUE

#FixMateInformation
java -Xmx8g -jar $PICARD FixMateInformation \
	INPUT=$OUT.sorted.bam \
	OUTPUT=$OUT.fxmt.bam \
	VALIDATION_STRINGENCY=LENIENT \
	CREATE_INDEX=TRUE

#MarkDuplicates
java -Xmx8g -jar $PICARD MarkDuplicates \
	INPUT=$OUT.fxmt.bam \
	OUTPUT=$OUT.mkdup.bam \
	METRICS_FILE=$OUT.metrics \
	VALIDATION_STRINGENCY=LENIENT \
	CREATE_INDEX=TRUE \
	MAX_FILE_HANDLES_FOR_READ_ENDS_MAP=1000

#AddOrReplaceReadGroups
java -Xmx8g -jar $PICARD AddOrReplaceReadGroups \
	INPUT=$OUT.mkdup.bam \
	OUTPUT=$OUT.addrep.bam \
	VALIDATION_STRINGENCY=LENIENT \
	CREATE_INDEX=TRUE \
	RGID=$RDName \
	PL=Illumina \
	SM=$RDName \
	CN=BGI \
	LB=Illumina \
	PU=barcode


#VARIANT CALLING

#Reference Index
samtools faidx $REF.fa
rm $REF.dict
#Reference Dictionary (CreateSequenceDictionary)
java -Xmx8g -jar $PICARD CreateSequenceDictionary \
	REFERENCE=$REF.fa \
	OUTPUT=$REF.dict

#Realign Target (RealignerTargetCreator)
java -Xmx8g -jar $GATK \
	-T RealignerTargetCreator \
	-I $OUT.addrep.bam \
	-R $REF.fa \
	-o $OUT.intervals \
	-nt 8

#IndelRealigner
java -Xmx8g -jar $GATK \
	-T IndelRealigner \
	-I $OUT.addrep.bam \
	-R $REF.fa \
	-targetIntervals $OUT.intervals \
	-o $OUTrealn/$RDName.realn.bam
