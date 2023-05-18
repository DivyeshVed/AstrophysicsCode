#!/bin/bash

####Code to create gti files and extract lightcurve from files, modified to extract light curves from single exposures in an OBSID, mainly for GRS1915+105


#### get PROPID variable from python script 

PROPID=$1
MODETYPE=$2
INPUT=$3
OUTPUT=$4

FILES=pca/F*
FILTERFILETYPE=stdprod/*.xfl.gz


for p in $PROPID
do
	echo $p
	####Remove existing files to overwrite
	rm -f -- $p/gtifile
	rm -f -- $p/512lc_$OUTPUT

	####Make GTI file
	#echo $p/$FILTERFILETYPE
	maketime $p/$FILTERFILETYPE $p/gtifile "elv.gt.10.and.offset.lt.0.02.and.(TIME_SINCE_SAA > 30 || TIME_SINCE_SAA < 0.0)" name='NAME' value='VALUE' time='TIME' compact=no

	if [ $MODETYPE = 1 ]
	then
		echo "SB mode"

		saextrct $INPUT gtiorfile="APPLY" gtiandfile=$p/gtifile outroot=$p/512lc_$OUTPUT accumulate="ONE" timecol="TIME" columns="GOOD" binsz=0.001953125 printmode="LIGHTCURVE" lcmode="RATE" spmode="SUM" timemin="INDEF" timemax="INDEF" timeint="INDEF" chmin="INDEF" chmax="INDEF" chint="INDEF" chbin="INDEF"

	fi

done


