import glob
import sys
import re
import pandas as pd
from astropy.io import fits
from itertools import islice
from os import path
import os.path
import pickle
import numpy
from cal_int_rms import *

#### Code to get the GTI length, count rate, hardness ratio and obsdate for each observation.

propid = 'P70104/70104-02-02-00'
path = '/Users/erinhorbacz/Downloads/Research/testData/%s'%propid
## suf = _a, _b, _c, _d, or ""
suf = '_b'	##individual observation
log_qpo = True ##Check Q value; if Q not significant (< 2) do not log!

for pathname in glob.glob(path):

	#Get num PCU
	filename = (propid.split("/"))[1]
	filename = filename.replace("-", "")
	print(filename)
	pcu_path = '/Users/erinhorbacz/Downloads/Research/testData/%s/stdprod/x%s.xfl'%(propid, filename)

	with fits.open(pcu_path) as hdul:
	    scidata = hdul[1].data
	    scidata = scidata[scidata.NUM_PCU_ON != 0]
	    num_PCU = int(numpy.nanmean(scidata.NUM_PCU_ON))


	print(pathname)
	lc_file = '%s/128lc%s.lc'%(pathname, suf)
	if os.path.exists(lc_file):

		#calculate integrated rms
		datafile = '%s/128lc%s'%(path,suf)
		integrated_rms, rms_err = cal_int_rms('%s'%datafile, seglength = 2048, minfreq=0.1, maxfreq=64.0)
		print("INTEGRATED", integrated_rms)

		rows_list={} #list of dictionaries to turn into dataframe

		#### Get name of Standard2 file
		if suf == "":
			ind_obs = "total"
			fname = '%s/datamode_total.txt'%pathname
		else:
			ind_obs = suf.strip("_")
			fname = '%s/datamode.txt'%pathname

		#Get datamode
			##single bit mode
		if 'SB_' in open(fname).read():
			datamode = 'Single Bit'
			##event mode
		elif 'E_' in open(fname).read():
			datamode = 'Event Mode'
			##good xenon
		elif 'GoodXenon' in open(fname).read():
			datamode = 'Good Xenon'

		#get info from qpo_o.txt if it existst
		num_qpo = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		for j in range(len(num_qpo)):
			if os.path.exists('%s/qpo_fit%s/qpo_%i.txt'%(pathname, suf, j)):
				file = open('%s/qpo_fit%s/qpo_%i.txt'%(pathname, suf, j), 'r')
				lines = file.readlines()
				for i in range(1, len(lines)):
					line = lines[i].split("\t")
					freq = "%.5f"%float(line[0])
					Q = "%.5f"%float(line[2])
					qpo_rms = "%.5f"%float(line[3])
					sig = "%.5f"%float(line[5])
					best_chi = "%.5f"%float(line[6])
				file.close()
				#get best model: this should work fine as long as all code above worked
				if os.path.exists('%s/qpo_fit%s/best_model.txt'%(pathname, suf)):
					model_file = open('%s/qpo_fit%s/best_model.txt'%(pathname, suf), 'r')
					lines = model_file.readlines()
					best_fit_mod = lines[0]
				else:
					print('BEST MODEL TXT DOESNT EXIST: go back to compile dataframe and check error')
				print('Finished writing first half of log!...')
				break
			else:
				#if Q value was less than 2 , no need for other data (QPO insignificant)
				log_qpo = False
				print("Q value not significant. This file doens't exist: %s/qpo_fit%s/qpo_%i.txt"%(pathname, suf, j))

		##Create a second dictionary with the following info from compile_dataframe_info
		if log_qpo:
			with open('%s/qpo_fit%s/compile_dataframe_info.pkl'%(pathname, suf), 'rb') as f:
			#dict2 = pickle.load(f)
				data = pickle.load(f)
				#data = data.tail(1)
				#print(data)
				name = data.at[0, 'NAME']
				obsid = data.at[0, "OBSID"]
				ind_obs = data.at[0, "INDIVIDUAL OBS"]
				date = data.at[0, "OBSDATE"]
				time = data.at[0, "TIME"]
				gti = data.at[0, "GTI"]
				count = data.at[0, "COUNTRATE"]
				hr = data.at[0, "HARDNESS_RATIO"]
				classification = data.at[0, "CLASSIFICATION"]
				dict2 = {'NAME': name, 'OBSID':obsid, 'INDIVIDUAL OBS': ind_obs, 'OBSDATE':date, 'TIME': time, 'GTI':gti, 'COUNTRATE':count, 'HARDNESS_RATIO':hr}
				rows_list.update(dict2)
				#rows_list.update(pickle.load(f))
				print('Finished writing second half of log!...')

			##Create dictionary 1 with following info
			dict1={'DATA MODE': datamode, 'QPO FREQ': freq, 'Q VAL': Q, 'SIGNIFICANCE': sig, 'QPO RMS': qpo_rms, 'INTEGRATED RMS': integrated_rms, "CLASSIFICATION": classification, 'NUM PCU': num_PCU, 'BEST MODEL': best_fit_mod, 'BEST RED CHI SQUARED': best_chi}
			rows_list.update(dict1)
			print(rows_list)

			df = pd.DataFrame(rows_list, index = [0])	##turn dictionaries into a dataframe

			if os.path.exists('/Users/erinhorbacz/Downloads/Research/testData/QPO_log.pkl'):	##Check to make sure log file exists
				fp = pd.read_pickle('/Users/erinhorbacz/Downloads/Research/testData/QPO_log.pkl')
				if (ind_obs in (list(fp['INDIVIDUAL OBS']))) and (obsid in (list(fp['OBSID']))): ##Check if QPO being logged has already been logged (duplicate)
					for obs in (list(fp['OBSID'])):
						for ind in (list(fp['INDIVIDUAL OBS'])):
							if obs == obsid and ind == ind_obs:
								print(name, obsid, ind_obs)
								print(list(fp['OBSID']))
								print("YOU ALREADY LOGGED THIS QPO. WOULD YOU LIKE TO OVER WRITE IT?")
								response = input("Enter Y or N: ")
								if response == "Y":
									print(fp.index)
									for index in fp.index:
										if (data.at[index, "NAME"] == name) and (data.at[index, "INDIVIDUAL OBS"] == ind_obs):		##replace duplicate with current version
											replace_index = index
											print(replace_index)
											#replace_row = rows_list
											fp = fp.drop(replace_index)
											fp.loc[replace_index] = [name, obsid, ind_obs, date, time, gti, count, hr, datamode, freq, Q, sig, qpo_rms, integrated_rms, classification, num_PCU, best_fit_mod, best_chi]
											print(fp)
											fp.to_pickle('/Users/erinhorbacz/Downloads/Research/testData/QPO_log.pkl')
											#fp = Insert_row(replace_index, fp, replace_row)
											#fp.to_pickle('/Users/erinhorbacz/Downloads/Research/testData/QPO_log.pkl')
											#fp = fp.append(pd.DataFrame(df, index = [replace_index]))
											print("Rewrote QPO in log!")
											break
								else:
									print("QPO not logged")	##chose not to overwrite the QPO
									break

				else:	##if the QPO being logged is not a duplicate
					##log QPO
					print("LOGGING")
					fp = fp.append(df, ignore_index = True)
					print(fp)
					fp.to_pickle('/Users/erinhorbacz/Downloads/Research/testData/QPO_log.pkl')
					print("logged QPO!")
			else:	##if log file does not exist
				##create log and log QPO
				print(df)
				df.to_pickle('/Users/erinhorbacz/Downloads/Research/testData/QPO_log.pkl')
				print("created log file called QPO_log and logged QPO!")
		else:
			print("QPO not logged")
