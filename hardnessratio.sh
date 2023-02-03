#!/bin/bash

### Run pcabackest and then saextrct to get the background and source light curve in desired energy bands
### get variables from python script 
PATHNAME=$1
CHNINT1_LOW=$2
CHNINT1_HIGH=$3
CHNINT2_LOW=$4
CHNINT2_HIGH=$5
STD2FILENAME=$6
FILTERFILENAME=$7
###Run code 
echo $PATHNAME
echo $STD2FILENAME
echo $FILTERFILENAME

pcabackest
#Run pcabackest
pcabackest infile=$STD2FILENAME outfile=$PATHNAME/pca/bkg.xdf modelfile=/Users/rohanpunamiya/Desktop/pca_bkgd_cmbrightvle_eMv20051128.mdl filterfile=$FILTERFILENAME interval=16 layers=no gaincorr=no fullspec=no saahfile=/Users/rohanpunamiya/Desktop/pca_saa_history.gz
##Get background lc in 2 different energy bands
saextrct $PATHNAME/pca/bkg.xdf gtiorfile="APPLY" gtiandfile=$PATHNAME/gtifile outroot=$PATHNAME/pca/bkg_chb accumulate="ONE" timecol="TIME" columns="GOOD" binsz=16 printmode="LIGHTCURVE" lcmode="RATE" spmode="SUM" timemin="INDEF" timemax="INDEF" timeint="INDEF" chmin="INDEF" chmax="INDEF" chint=$CHNINT1_LOW-$CHNINT1_HIGH chbin=$CHNINT1_LOW-$CHNINT1_HIGH
saextrct $PATHNAME/pca/bkg.xdf gtiorfile="APPLY" gtiandfile=$PATHNAME/gtifile outroot=$PATHNAME/pca/bkg_chc accumulate="ONE" timecol="TIME" columns="GOOD" binsz=16 printmode="LIGHTCURVE" lcmode="RATE" spmode="SUM" timemin="INDEF" timemax="INDEF" timeint="INDEF" chmin="INDEF" chmax="INDEF" chint=$CHNINT2_LOW-$CHNINT2_HIGH chbin=$CHNINT2_LOW-$CHNINT2_HIGH
##Get source lc in 2 different energy bands using Std2 data
saextrct $STD2FILENAME gtiorfile="APPLY" gtiandfile=$PATHNAME/gtifile outroot=$PATHNAME/pca/src_chb accumulate="ONE" timecol="TIME" columns="GOOD" binsz=16 printmode="LIGHTCURVE" lcmode="RATE" spmode="SUM" timemin="INDEF" timemax="INDEF" timeint="INDEF" chmin="INDEF" chmax="INDEF" chint=$CHNINT1_LOW-$CHNINT1_HIGH chbin=$CHNINT1_LOW-$CHNINT1_HIGH
saextrct $STD2FILENAME gtiorfile="APPLY" gtiandfile=$PATHNAME/gtifile outroot=$PATHNAME/pca/src_chc accumulate="ONE" timecol="TIME" columns="GOOD" binsz=16 printmode="LIGHTCURVE" lcmode="RATE" spmode="SUM" timemin="INDEF" timemax="INDEF" timeint="INDEF" chmin="INDEF" chmax="INDEF" chint=$CHNINT2_LOW-$CHNINT2_HIGH chbin=$CHNINT2_LOW-$CHNINT2_HIGH

