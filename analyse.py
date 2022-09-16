# This code is the second one to the run in the pipeline. 
# This code is used to extract the powerspectrum using the lightcurve data that was extracted in the previous step of the pipeline. 
# Once again, you can run this code using the simple command on your terminal window: python3 anaylse.py
# Before running this code, always remember to initialize HEASoft using the following command in your terminal: heainit
# You must manually change the prnb and the obsid folder path on line 24. 

import numpy #Libray that is used for wokring with array
import scipy #Library used for scientific and technical computing
import time #A way of representing time in code
import glob #A module used to retrieve file names or paths mathcing a specific pattern
import os #Module provides functions for creating and removing a directory, fetching it contents, changing and identifying the current directory
import sys #Module that proivdes functions ot manupilate differents parts of the runtime python environment
from pylab import * #Module that bulk imports matplotlib
import matplotlib.pyplot as plt #Importing matplotlib under a certian name
from powerspec import *
import pickle
from os.path import exists


# Setting variables

# Taking input from the user that will be the prnb number.
# prnbFolder = sys.argv[1]
# Constructing the path for the obsid folder.
# path = '/Users/rohanpunamiya/Documents/%s' %prnbFolder
# Getting a list of all the obsid folders in the prnb folder.
# obsidList = os.listdir(path)
# Constructing the path to all the propids.
# propidPath = path + '/*'
def analyse(path,obsidList, propidPath):
	# Setting the seglength variable. 
	seglength = 2048
	# Calculating the time that the function takes. 
	zero_time = time.time()

	# Making a list of suffixes that can be used as the file names.
	suf = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p']

	# Printing the path varibale.
	print(propidPath)
	# Iterating through the files that are at this path.
	for pathname in glob.glob(propidPath):
		print(pathname)
		# Checking if the 512lc file exists in the folder.
		if os.path.exists('%s/512lc.lc'%(pathname)) == True:
			datafile = '%s/512lc'%(pathname)
			# Printing the data file that was made. 
			print(datafile)

			#Read each fits file into text. Initializing the time variable. 
			start_time = time.time()
			# Reading the fits file.
			readfits(datafile)
			# Printing the amount of time taken to read through the fits file. 
			print("---Read file in %s seconds ---" %(time.time() - start_time))

			#Generate powerspectrum for each file and save results. Starting the time variable.
			start_time = time.time()
			# Calculating the frequency, spectrum, and the error, using the powerspectrum function, and the fits files as the input for the function. 
			freq, spec, err = powerspec(datafile, seglength)
			# Making the data variable that will holf the frequency and spectrum values using the numpy library. 
			data = numpy.column_stack((freq,spec))
			# Saving the data from the powerspectrum numpy column a text filie called powerspectrum. 
			numpy.savetxt('%s_powerspec_%i.txt'%(datafile,seglength),data,delimiter='\t',newline='\n')
			# Printing out a line to tell the amount of time taken to the calculate the power spectrum. 
			print("---Calculated power spectra in %s seconds ---" %(time.time() - start_time))

			####Plot power spectrum. This uses the fractional rms variance. 
			x, y, z = powerspec(datafile, seglength,norm='frac_rms')
			plt.loglog(x, y*x)
			plt.title("Power Spectrum")
			plt.xlabel("Frequency")
			plt.ylabel("Leahy Normalisation")
			plt.savefig('%s_powerspec_%i.png'%(datafile,seglength))
			plt.close()

	# Taking the total amount of time to carry out all the functions, and complete the script.  
	print("---Total time taken is %s seconds ---" %(time.time() - zero_time))

	# Checking that the code ran correctly: looking for the 512lc.txt and 512lc.lc folder in the obsid folder
	# Loading the pkl file.
	data = pickle.load(open("/Users/rohanpunamiya/Documents/testDataFrame.pkl","rb"))
	# Splitting the obsid path to find the just the obsid
	obsidName = path.split("/")[-1]
	for obsid in obsidList:
		# Going into the obsid directory
		os.chdir(path + '/' + obsid)
		# Checking for the txt folder
		datamode_exists = exists('512lc.txt')
		# Checking for the lc file
		lc_exists = exists('512lc.lc')
		# If qpo_fit folder exists, then change the column under qpo_fit_code.py to yes
		if datamode_exists == True and lc_exists == True:
			# Finding the index of the obsid in the dataframe
			idx = int(data[data["OBSID"]== str(obsidName)].index.values)
			# Replacing the qpo_fit_code.py column to yes at the particular row index
			data.loc[idx,'Ran analyse.py'] = 'Yes'
	data.to_pickle("/Users/rohanpunamiya/Documents/testDataFrame.pkl")
