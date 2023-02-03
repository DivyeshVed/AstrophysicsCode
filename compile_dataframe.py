import numpy
import subprocess
import glob
import sys
import re
import pandas as pd
from astropy.io import fits
from itertools import islice
import matplotlib.pyplot as plt
import os
import pickle

#### Code to get the GTI length, count rate, hardness ratio and obsdate for each observation.
### Use this code when Standard2 files are found in datamode.txt

index_error = []
filenotfound_error = []
# datalist = pickle.load(open("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/6sigma_QPO_list.pkl","rb"))

# Taking input from the user. This input is the prnb folder name. 
prnbFolder = sys.argv[1]
# Getting the path of the data. This is the path to the prnb folder. 
prnbPath = '/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/%s' %prnbFolder
# prnbPath = "/Users/rohanpunamiya/Desktop/%s" %prnbFolder
# Maing a list of the obsid folders in the prnb folder. 
obsidList = os.listdir(prnbPath)
# Checking if the .DS_Store exists as an obsid folder. 
if '.DS_Store' in obsidList:
    # Deleting it if that item exists.
	obsidList.remove('.DS_Store')

# obsidList = datalist.loc[:,"OBSID"]
f = '512lc.lc'
# ## ind_obs = _a, _b, _c, _d, or ""
# ind_obs1 = '_b'

# #Determine name of datamode file
# if ind_obs1 == '':
# 	datamode_total = "_total"
# 	ind_obs = 'total'
# else:
# 	datamode_total = ""
# 	ind_obs = ind_obs1[1]
# 	print(ind_obs)
data = pickle.load(open("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/compile_dataframe_info.pkl","rb"))

#### Start code
rows_list=[] #list of dictionaries to turn into dataframe
for num in range(len(obsidList)):
	obsid = obsidList[num]
	# prnbFolder = "P" + obsid[0:5]
	pathname = "/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/" + prnbFolder + "/" + obsid
	print("pathname:" + pathname)
	# pathname = "/Users/rohanpunamiya/Desktop/" + prnbFolder + "/" + obsid
# for pathname in glob.glob(prnbPath):
	qpo_path = '%s/%s'%(pathname, f)
	print("This is the prnb folder path: " + pathname)

	#### Get OBSID from path
	obs = obsid.replace('-', '')

	#### Get GTI length from lightcurve. What is 
	gti_start =[]
	gti_end=[]
	with fits.open(qpo_path) as hdul:
		gtidata = hdul[2].data
		gtilen = []
		for i in range(0,len(gtidata)):
			gtilen.append(gtidata[i][1] - gtidata[i][0])
		gti = int(sum(gtilen))

	#### Get mean count rate normalised per pcu from stdprod data
	pathname2 = '%s/stdprod/xp%s_n1.lc.gz'%(pathname,obs)
	#pathname2 = '%s/stdprod/xp10067010100_n1.lc.gz'%pathname
	print("This goes to the file with the mean count rate: " + pathname2)
	count = 0
	try:
		with fits.open('%s'%pathname2) as lc: #Opening a fits file
			scidata = lc[1].data
			count = int(numpy.nanmean(scidata.RATE))
	except FileNotFoundError:
		filenotfound_error.append(obsid)
		continue

	#### Get name of Standard2 file
	fname = '%s/datamode.txt'%(pathname)
	print("fname:" + fname)
	s = 'Standard2'
	f1 = open(fname)
	std2list=[]
	for line in f1:
		print(line)
		if s in line:
			std2list.append((''.join(islice(f1,1))))
	f1.close()
	print("This is stdList:")
	print(std2list)
	lengthoflist = len(std2list)
	print("This is the length of std2list: ",lengthoflist)
	try:
		std2file = std2list[0]
	except IndexError:
		index_error.append(obsid)
		continue
	std2filenameSplit = std2file.split("/")
	std2filename = pathname + "/" + std2filenameSplit[-2] + "/" + std2filenameSplit[-1]

	#### Get name of filter file
	filterfile = open('%s/filter.txt'%pathname).readline()
	filterfileList = filterfile.split("/")
	filterfilename = pathname + "/" + filterfileList[-2] + "/" + filterfileList[-1]

	#print(filterfilename)

	date = None
	#### Get obsdate, epoch and assign correct channel intervals
	with fits.open(qpo_path) as hdul:
		mjd = hdul[1].header['MJDREFI']  + (hdul[1].header['TSTARTI']/86400)
		date = hdul[1].header['DATE-OBS']
		time = hdul[1].header['TIME-OBS']
		name = hdul[1].header['OBJECT']
		#print(mjd)

		#### channels given for 2-13keV and 13-30keV for each epoch
		if mjd < 50163:
			#print('epoch 1')
			chint1_low = '6'
			chint1_high = '48'
			chint2_low = '49'
			chint2_high = '109'
		elif 50163 <= mjd < 50188:
			#print('epoch 2')
			chint1_low = '5'
			chint1_high = '40'
			chint2_low = '41'
			chint2_high = '95'
		elif 50188 <= mjd < 51259:
			#print('epoch 3')
			chint1_low = '0'
			chint1_high = '35'
			chint2_low = '36'
			chint2_high = '81'
		elif 51259 <= mjd < 51677:
			#print('epoch 4')
			chint1_low = '0'
			chint1_high = '30'
			chint2_low = '31'
			chint2_high = '69'
		elif mjd >= 51677:
			#print('epoch 5')
			chint1_low = '0'
			chint1_high = '30'
			chint2_low = '31'
			chint2_high = '71'

	print(mjd, chint1_low, chint1_high, chint2_low, chint2_high)
	#### Extract files for calculating hardness ratio
	print("This is what is in the pathname variable:" + pathname)
	print('Starting background and lightcurve extraction')
	subprocess.call(['./hardnessratio.sh', pathname, chint1_low, chint1_high, chint2_low, chint2_high, std2filename, filterfilename])

	try: 
		#### Get values from the extracted files
		with fits.open('%s/pca/src_chb.lc'%pathname) as src_lowen:
			rate1 = src_lowen[1].data.RATE
		with fits.open('%s/pca/bkg_chb.lc'%pathname) as bkg_lowen:
			bkg1 = bkg_lowen[1].data.RATE
		netrate1 = numpy.nanmean(rate1-bkg1)
		#print(netrate1)

		with fits.open('%s/pca/src_chc.lc'%pathname) as src_hien:
			rate2 = src_hien[1].data.RATE
		with fits.open('%s/pca/bkg_chc.lc'%pathname) as bkg_hien:
			bkg2 = bkg_hien[1].data.RATE
		netrate2 = numpy.nanmean(rate2-bkg2)
		#print(netrate2)

		hr = numpy.round(netrate2/netrate1, 3)
		print('HR is', netrate2/netrate1)

		dict1={'NAME':name, 'OBSID':obsid, 'INDIVIDUAL OBS':obsid, 'OBSDATE':date, 'TIME':time, 'GTI':gti, 'COUNTRATE':count, 'HARDNESS_RATIO':hr}
		data = data.append(dict1, ignore_index = True)
		print(dict1)
	except FileNotFoundError:
		filenotfound_error.append(obsid)
		continue

data.to_pickle("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/compile_dataframe_info.pkl")
errorList = pd.DataFrame(filenotfound_error, columns = ["OBSID: fileNotFound"])
errorList.to_pickle("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/fileNotFoundErrorDataframe.pkl")
