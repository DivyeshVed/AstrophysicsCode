import numpy
import scipy
import time
import subprocess
import glob
import os
import sys
from itertools import islice
####Use this in-depth extraction of certain obsids.#####
####Code to extract lightcurves *from each exposure* from all the observations in a given PropID####

#following Yan et al 2012 for data reduction#

####Set variables
start_time = time.time() 
# propid = sys.argv[1] # Want to make this such that it is a text file that contains all the obsids.
#propid ='1915+105/P20186/20186-03-02-052'
path = '/Users/rohanpunamiya/Desktop/obds/93443-01-01-02'
files = '%s/datamode.txt'%path

print(path)

# We are not interested in creating the datamode.txt file again, thus we comment out the two lines below. 
print("Creating list of datamode files..")
subprocess.call(['./list.sh' , path])
print("DONE!")

suf = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p']

###Create list of filenames to be extracted
#### Using single bit mode as no energy information needed here, and has good time resolution.
for pathname in glob.glob(path):
	print(pathname)
	if 'SB_' in open('%s/datamode.txt'%pathname).read():
		modetype = '1'
		s = 'SB_'
		print('modetype is', 1)
	fname = '%s/datamode.txt'%pathname
	#print fname
	f1 = open('%s/sblist.txt'%pathname, 'w')
	f = open(fname)
	for line in f:
		if s in line:
			filename = (''.join(islice(f,1)))
			f1.write(filename)
	f1.close()
	f.close()

	###Make GTI and extract light curve

	with open('%s/sblist.txt'%pathname, 'r') as f:
		for i, line in enumerate(f):
			outputname = suf[i]
			inputname = line.strip()
			subprocess.call(['./makegti2.sh' , pathname, modetype, inputname, outputname])
		
print("extracted in", time.time()-start_time, "seconds")
	
