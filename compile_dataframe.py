import numpy
import subprocess
import glob
import sys
import re
import pandas as pd
from astropy.io import fits
from itertools import islice
import matplotlib.pyplot as plt

#### Code to get the GTI length, count rate, hardness ratio and obsdate for each observation.
### Use this code when Standard2 files are found in datamode.txt

path = '/Users/rohanpunamiya/Desktop/Data/P10067/10067-01-01-00'
f = '128lc_b.lc'
## ind_obs = _a, _b, _c, _d, or ""
ind_obs1 = '_b'


#Determine name of datamode file
if ind_obs1 == '':
	datamode_total = "_total"
	ind_obs = 'total'
else:
	datamode_total = ""
	ind_obs = ind_obs1[1]
	print(ind_obs)

#### Start code
rows_list=[] #list of dictionaries to turn into dataframe
for pathname in glob.glob(path):
	qpo_path = '%s/%s'%(pathname, f)
	print(pathname)

	#### Get OBSID from path
	string = pathname.split("/")
	#propid = string[-2]
	obsid = string[-1]
	obs = obsid.replace('-', '')

	#### Get GTI length from lightcurve
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
	print(pathname2)
	with fits.open('%s'%pathname2) as lc: #Opening a fits file
		scidata = lc[1].data
		count = int(numpy.nanmean(scidata.RATE))

	#### Get name of Standard2 file
	fname = '%s/datamode.txt'%(pathname)
	s = 'Standard2'
	f1 = open(fname)
	std2list=[]
	for line in f1:
		if s in line:
			std2list.append((''.join(islice(f1,1))))
	f1.close()
	lengthoflist = len(std2list)
	print("This is the length of std2list: ",lengthoflist)
	std2filename = std2list[1] #workaround if multiple std2files present
	#print(std2filename)

	#### Get name of filter file
	filterfilename = open('%s/filter.txt'%pathname).readline()
	#print(filterfilename)

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

	#print(mjd, chint1_low, chint1_high, chint2_low, chint2_high)
	#### Extract files for calculating hardness ratio
	print('Starting background and lightcurve extraction')
	subprocess.call(['./hardness_ratio.sh', path, chint1_low, chint1_high, chint2_low, chint2_high, std2filename, filterfilename])

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
	#print('HR is', netrate2/netrate1)

	dict1={'NAME': name, 'OBSID':obsid, 'INDIVIDUAL OBS': ind_obs, 'OBSDATE':date, 'TIME': time, 'GTI':gti, 'COUNTRATE':count, 'HARDNESS_RATIO':hr}
	rows_list.append(dict1)



print(rows_list)
df = pd.DataFrame(rows_list)
df.to_pickle('%s/qpo_fit%s/compile_dataframe_info.pkl'%(pathname, ind_obs1))
#print(df)
