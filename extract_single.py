# This is the first code that is to be run in the pipeline. 
# This code extracts the light curve data from the data that was downloaded from the NASA archives.
# Remember to initialize HEASoft before running this code using the following command in yout terminal: heainit
# To run this code, use the following command: python3 extract.py 
# You need to change the prnb folder and the obsid that you want to run the code on manually on line 22 of the code.

import numpy
import scipy
import time
import subprocess
import glob
import sys
from itertools import islice
import os
import pandas as pd
import pickle
from os.path import exists

# def extract(path, propidList, propidPath): 
# Taking input from the user. The first input is the prnb number
prnbFolder = sys.argv[1]
obsidFolder = sys.argv[2]
# The propid refers to the proppsal ID that we want to run the code on. In this line, using the asterisk is using the widlcard, thus you can calling this code
# on all the lines in the folder with the name of the proposal ID. 
# propid = prnbFolder + '/*'
#propid = sys.argv[1]
#propid ='GX339-4/P70110/7*'
prnbAndObsid = prnbFolder + '/' + obsidFolder
# The path refers to the place where you can find the proposal ID folder. This path is attached to the propsal ID folder name, with it being at the end. 
path = '/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/%s'%prnbAndObsid

# Returns the time taken to run the code. 
start_time = time.time()
# This refers to the file name that we are going to create in each of the proposal ID folders, as we are given the path above. 
files = '%s/datamode.txt'%path
# Output on the terminal indicating to the user than the code has began running.
print('Creating list of datamode files..')
# The subprocess module allows you to pawn new processes, connecting their inputs, outputs and many other things, but finally returning the output code. 
# This line will run the commands given in the first arguement. In this case, it will go into the current folder (the one you run the code in AstrophysicsCode) and
# it will look for a file with the bame list.sh, and then it will run the commands in this file. 
subprocess.call(['./list.sh' ,path])
# It will print this otuput to the terminal once the commands have run. 
print('DONE!')

###Create list of filenames to be extracted
# THe glob module finds all the pathnames matching a specified pattern. Return a list of empty path names that match pathname.
for pathname in glob.glob(path):
	# Pritning the pathname
	print(pathname)
	# Looking for the expression SB_ in the datamode file. If it does, then  assigning the modetype to 1
	if 'SB_' in open('%s/datamode.txt'%pathname).read():
		modetype = '1'
		s = 'SB_'
		print( 'modetype is', 1)
	# Looking for the expression E_125 in the datamode file. If it does, then  assigning the modetype to 2
	if 'E_125' in open('%s/datamode.txt'%pathname).read():
		modetype = '2'
		s = 'E_125'
		print( 'modetype is', 2)
	# Looking for the expression E_500 in the datamode file. If it does, then  assigning the modetype to 3
	elif 'E_500' in open('%s/datamode.txt'%pathname).read():
		modetype = '2'
		s = 'E_500'
		print( 'modetype is', 2)
	# Looking for the expression E_250 in the datamode file. If it does, then  assigning the modetype to 4
	elif 'E_250' in open('%s/datamode.txt'%pathname).read():
		modetype = '2'
		s = 'E_250'
		print( 'modetype is', 2)
	# Looking for the expression GoodXenon in the datamode file. If it does, then  assigning the modetype to 5
	elif 'GoodXenon' in open('%s/datamode.txt'%pathname).read():
		modetype = '3'
		s = 'GoodXenon'
		print( 'modetype is', 3)
	fname = '%s/datamode.txt'%pathname
	#print fname
	f1 = open('%s/sblist.txt'%pathname, 'w')
	f = open(fname)
	for line in f:
		if s in line:
			if modetype == '1':
				if '249' not in line: #to make sure data over 30keV is excluded
					filename = (''.join(islice(f,1)))
					f1.write(filename)

			else:
				filename = (''.join(islice(f,1)))
				f1.write(filename)
	f1.close()
	f.close()

	###Make GTI and extract light curve
	subprocess.call(['./makegti.sh' , pathname, modetype])

print('extracted in', time.time()-start_time, "seconds")

# # Checking that the code ran correctly: looking for the datamode.txt file in the obsid folder
# # Loading the pkl file.
# data = pickle.load(open("/Users/rohanpunamiya/Documents/dataTable.pkl","rb"))
# # data = pickle.load(open("/Users/rohanpunamiya/Documents/testDataFrame.pkl","rb"))
# # Splitting the obsid path to find the just the obsid
# # obsidName = path.split("/")[-1]
# # Going into the obsid directory
# for id in propidList:
# 	os.chdir(propidPath + "/" + id)
# 	# Checking for the qpo_fit folder
# 	datamode_exists = exists('datamode.txt')
# 	# If qpo_fit folder exists, then change the column under qpo_fit_code.py to yes
# 	if datamode_exists == True:
# 		# Finding the index of the obsid in the dataframe
# 		idx = int(data[data["OBSID"]== str(id)].index.values)
# 		# Replacing the qpo_fit_code.py column to yes at the particular row index
# 		data.loc[idx,'Ran extract.py'] = 'Yes'
# data.to_pickle("/Users/rohanpunamiya/Desktop/AstrophysicsCode/dataTable.pkl")
# # data.to_pickle("/Users/rohanpunamiya/Documents/testDataFrame.pkl")
