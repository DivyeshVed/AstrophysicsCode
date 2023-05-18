import numpy #Libray that is used for wokring with array
import scipy #Library used for scientific and technical computing
import time #A way of representing time in code
import glob #A module used to retrieve file names or paths mathcing a specific pattern
import os #Module provides functions for creating and removing a directory, fetching it contents, changing and identifying the current directory
import sys #Module that proivdes functions ot manupilate differents parts of the runtime python environment
from pylab import * #Module that bulk imports matplotlib
import matplotlib.pyplot as plt #Importing matplotlib under a certian name
from powerspec import *

'''
10066-01-01-00
10067-01-01-00
30046-01-08-00
30046-01-12-00
40017-02-01-00
40017-02-06-00
40017-02-09-02
40017-02-16-01
40017-02-16-02
40019-04-02-00
40019-04-05-07
60417-01-03-00
70104-02-02-00
90030-01-46-00
93443-01-01-02 '''

####Set variables
#seglength = int(sys.argv[2])
seglength = 2048
#propid ='1915+105/P20186/20186-03-02-052'
# propid = sys.argv[1]
path = '/Users/rohanpunamiya/Desktop/obds/90030-01-46-00'
zero_time = time.time()

suf = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p']

print(path)
for pathname in glob.glob(path):
	print(pathname)
	for i in range(0,len(suf)):
		if os.path.exists('%s/512lc_%s.lc'%(pathname,suf[i])) == True:
			datafile = '%s/512lc_%s'%(pathname,suf[i])
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
			plt.loglog(freq, spec)
			plt.title("Power Spectrum")
			plt.xlabel("Frequency")
			plt.ylabel("Power (Leahy Normalised)")
			plt.savefig('%s_powerspec_%i.png'%(datafile,seglength))
			plt.close()

print("---Total time taken is %s seconds ---" %(time.time() - zero_time))
