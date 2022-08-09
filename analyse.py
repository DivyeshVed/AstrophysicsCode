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


####Set variables
#seglength = int(sys.argv[2])
seglength = 2048
#propid ='1915+105/P20186/20186-03-02-052'
propid = 'P10065/10065-02-01-00'
path = '/Users/rohanpunamiya/Desktop/Data/%s' %propid
zero_time = time.time()

suf = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p']

print(path)
for pathname in glob.glob(path):
	print(pathname)
	if os.path.exists('%s/512lc.lc'%(pathname)) == True:
		datafile = '%s/512lc'%(pathname)
		print(datafile)

		#Read each fits file into text
		start_time = time.time()
		readfits(datafile)
		print("---Read file in %s seconds ---" %(time.time() - start_time))

		#Generate powerspectrum for each file and save results
		start_time = time.time()
		freq, spec, err = powerspec(datafile, seglength)
		data = numpy.column_stack((freq,spec))
		numpy.savetxt('%s_powerspec_%i.txt'%(datafile,seglength),data,delimiter='\t',newline='\n')
		print("---Calculated power spectra in %s seconds ---" %(time.time() - start_time))

		####Plot power spectrum
		x, y, z = powerspec(datafile, seglength,norm='frac_rms')
		plt.loglog(x, y*x)
		plt.title("Power Spectrum")
		plt.xlabel("Frequency")
		plt.ylabel("Leahy Normalisation")
		plt.savefig('%s_powerspec_%i.png'%(datafile,seglength))
		plt.close()

print("---Total time taken is %s seconds ---" %(time.time() - zero_time))

# Checking that the code ran correctly: looking for the 512lc.txt and 512lc.lc folder in the obsid folder
# Loading the pkl file.
data = pickle.load(open("/Users/rohanpunamiya/Desktop/AstrophysicsCode/dataTable.pkl","rb"))
# Splitting the obsid path to find the just the obsid
obsidName = path.split("/")[-1]
# Going into the obsid directory
os.chdir(path)
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
data.to_pickle("/Users/rohanpunamiya/Desktop/AstrophysicsCode/dataTable.pkl")
