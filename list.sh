#!/bin/bash

####Code to append filename and corresponding DATAMODE keyword from pca subdir into .txt file


#### get PROPID variable from python script
PROPID=$1
FILES=pca/F*
FILTERFILETYPE=stdprod/*.xfl.gz
FILTERLIST=filter.txt
FILELIST=datamode.txt

for p in $PROPID
do
	echo $p
	####Remove existing files to overwrite
	rm -f -- $p/$FILELIST
	rm -f -- $p/$FILTERLIST
	echo 'cleared files'

	####Append filterfile to filter.txt
	echo $p/$FILTERFILETYPE >> $p/$FILTERLIST

	###Get DATAMODE keyword of each file and append to datamode.txt
	for f in $p/$FILES
	do
		ftlist $f[1] k include=datamode >> $p/$FILELIST
		echo $f >> $p/$FILELIST
		echo 'created datamode'	
	done
done
