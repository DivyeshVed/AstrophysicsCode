# AstrophysicsCode

The idea is to create a pipeline that can be used to extract a powerspectrum from NASA archived data. 
From there, this powerspectrum is fit using appropriate models using XSPEC.
Based on the fitting parameters and models, we are able to gain some information on the presence of a QPO in the system.

The files should be run in this order to create a proper pipeline for analyzing the data downloaded:

Before any code is run:
We create a file called allCodes.txt, which holds all the codes from the NASA website. As putting them in a text file makes it easier to work with in terms of removing lines. The file will contain all the file download codes from the NASA website, including the lines of code used to download data that we don't need.

1. Postdownload.py - this file is used to clean up the data that is downloaded. It helps get rid of the slue data, and it helps clear out any data that we don't want to analyse, or is not relevant to us. It does this using two functions: lineExtractor and obsidExtractor. We create a text file called codesToDownload. This file will contain all the codes that need be run on your terminal, which will download all the data from the NASA archives that we want. 
We first read in the allCodes.txt file, and run the line extractor on this file, and have the output go into the codesToDownload.txt file.

