#!/bin/bash

####Code to create gti files and extract lightcurve from files


#### get PROPID variable from python script

PROPID=$1
MODETYPE=$2

FILES=pca/F*
FILTERFILETYPE=stdprod/*.xfl.gz
FILTERLIST=filter.txt
FILELIST=datamode.txt

for p in $PROPID
do
	echo $p
	####Remove existing files to overwrite
	rm -f -- $p/gtifile

	####Make GTI file
	#echo $p/$FILTERFILETYPE
	maketime $p/$FILTERFILETYPE $p/gtifile "elv.gt.10.and.offset.lt.0.02.and.(TIME_SINCE_SAA > 30 || TIME_SINCE_SAA < 0.0)" name='NAME' value='VALUE' time='TIME' compact=no

	if [ $MODETYPE = 1 ]
	then
		echo "SB mode"
		#saextrct @$p/sblist.txt gtiorfile="APPLY" gtiandfile=$p/gtifile outroot=$p/64lc accumulate="ONE" timecol="TIME" columns="GOOD" binsz=0.015625 printmode="LIGHTCURVE" lcmode="RATE" spmode="SUM" timemin="INDEF" timemax="INDEF" timeint="INDEF" chmin="INDEF" chmax="INDEF" chint="INDEF" chbin="INDEF"

		#saextrct @$p/sblist.txt gtiorfile="APPLY" gtiandfile=$p/gtifile outroot=$p/128lc accumulate="ONE" timecol="TIME" columns="GOOD" binsz=0.0078125 printmode="LIGHTCURVE" lcmode="RATE" spmode="SUM" timemin="INDEF" timemax="INDEF" timeint="INDEF" chmin="INDEF" chmax="INDEF" chint="INDEF" chbin="INDEF"

		saextrct @$p/sblist.txt gtiorfile="APPLY" gtiandfile=$p/gtifile outroot=$p/512lc accumulate="ONE" timecol="TIME" columns="GOOD" binsz=0.001953 printmode="LIGHTCURVE" lcmode="RATE" spmode="SUM" timemin="INDEF" timemax="INDEF" timeint="INDEF" chmin="INDEF" chmax="INDEF" chint="INDEF" chbin="INDEF"

	fi

	if [ $MODETYPE = 2 ]
	then
		echo "Event mode"
		#seextrct @$p/sblist.txt gtiorfile="APPLY" gtiandfile=$p/gtifile outroot=$p/64lc bitfile='/Users/rohanpunamiya/Desktop/AstrophysicsCode/bitfile_M' timecol="TIME" columns="Event" binsz=0.015625 printmode="LIGHTCURVE" lcmode="RATE" spmode="SUM" timemin="INDEF" timemax="INDEF" timeint="INDEF" chmin="INDEF" chmax="INDEF" chint=0-69 chbin="INDEF"

		#seextrct @$p/sblist.txt gtiorfile="APPLY" gtiandfile=$p/gtifile outroot=$p/128lc bitfile='/Users/rohanpunamiya/Desktop/AstrophysicsCode/bitfile_M' timecol="TIME" columns="Event" binsz=0.0078125 printmode="LIGHTCURVE" lcmode="RATE" spmode="SUM" timemin="INDEF" timemax="INDEF" timeint="INDEF" chmin="INDEF" chmax="INDEF" chint=0-69 chbin="INDEF"

		seextrct @$p/sblist.txt gtiorfile="APPLY" gtiandfile=$p/gtifile outroot=$p/512lc bitfile='/Users/rohanpunamiya/Desktop/AstrophysicsCode/bitfile_M' timecol="TIME" columns="Event" binsz=0.001953 printmode="LIGHTCURVE" lcmode="RATE" spmode="SUM" timemin="INDEF" timemax="INDEF" timeint="INDEF" chmin="INDEF" chmax="INDEF" chint=0-69 chbin="INDEF"

	fi

	if [ $MODETYPE = 3 ]
	then
		echo "Good Xenon"
		make_se -i $p/sblist.txt -p $p/event
		#seextrct $p/event_gx0 gtiorfile="APPLY" gtiandfile=$p/gtifile outroot=$p/64lc bitfile='-' timecol="TIME" columns="Event" binsz=0.015625 printmode="LIGHTCURVE" lcmode="RATE" spmode="SUM" timemin="INDEF" timemax="INDEF" timeint="INDEF" chmin="INDEF" chmax="INDEF" chint=0-69 chbin="INDEF"

		#seextrct $p/event_gx0 gtiorfile="APPLY" gtiandfile=$p/gtifile outroot=$p/128lc bitfile='-' timecol="TIME" columns="Event" binsz=0.0078125 printmode="LIGHTCURVE" lcmode="RATE" spmode="SUM" timemin="INDEF" timemax="INDEF" timeint="INDEF" chmin="INDEF" chmax="INDEF" chint=0-69 chbin="INDEF"

		seextrct $p/event_gx0 gtiorfile="APPLY" gtiandfile=$p/gtifile outroot=$p/512lc bitfile='-' timecol="TIME" columns="Event" binsz=0.001953 printmode="LIGHTCURVE" lcmode="RATE" spmode="SUM" timemin="INDEF" timemax="INDEF" timeint="INDEF" chmin="INDEF" chmax="INDEF" chint=0-69 chbin="INDEF"
	fi

done
