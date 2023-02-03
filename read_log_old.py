import numpy
import re
import glob
from powerspec import *
import sys
import pickle
import pandas as pd
import os

#### Make sure to run qpo_fit_code.py before running this code, otherwise there wont be any log files for this code to read!

# Loading the freqeuencyTable.pkl file to pick out prnb and obsid
data = pickle.load(open("/Users/rohanpunamiya/Dropbox (GaTech)/NS_Data/CygX2/frequencyTable.pkl","rb"))
columnHeader = ["OBSID", "Best fit model", "RCS", "Sig","Qval"]
df = pd.DataFrame(columns = columnHeader)
for idx in data.index:
	data = pickle.load(open("/Users/rohanpunamiya/Dropbox (GaTech)/NS_Data/CygX2/frequencyTable.pkl","rb"))
	# Taking input from the user. This input is the prnb folder name. 
	prnbFolder = data["PRNB"][idx]
	# Getting the particular obsid
	obsidFolder = data["OBSID"][idx]
	# Getting the path of the data. This is the path to the prnb folder. 
	prnbPath = '/Users/rohanpunamiya/Dropbox (GaTech)/NS_Data/CygX2/%s/%s' %(prnbFolder, obsidFolder)
	f = '512lc'
	seglength = 1024


	models = ['3lor', '4lor', '5lor']
	num_lor_dict = {'3lor':4 , '4lor':5 , '5lor':6}
	#models = ['4lor']


	for p in glob.glob(prnbPath):
		qpo_fit_path = '%s/qpo_fit'%(p)
		# NQF - No qpo fit
		if (not(os.path.exists(qpo_fit_path))):
			df.loc[idx, 'OBSID'] = obsidFolder
			df.loc[idx, 'Best fit model'] = "NQF"
			df.loc[idx, 'RCS'] = "NQF"
			df.loc[idx, 'Sig'] = "NQF"
			df.loc[idx, 'Qval'] = "NQF"
			continue
		print("QPO Fit Path: " + str(qpo_fit_path))
		model_dict ={}

		ps_file = '%s/%s_fracrms_ps_%i.txt'%(qpo_fit_path,f,seglength)

		freq1, pow1, err1 = numpy.genfromtxt('%s'%ps_file,delimiter='\t', unpack=True)
		freq_int = freq1[1] - freq1[0]

		for m in models:
			filepath = '%s/%s_%i_%s_log.log'%(qpo_fit_path, f, seglength, m)
			if (os.path.exists(filepath)):
				with open(filepath, 'r') as file:
					lines = file.readlines()

					#### Calculate reduced chi squared
					x = [lines for lines in lines if "Null hypothesis" in lines]
					dof = (float(x[-1].split(" ")[7]))

					y = [lines for lines in lines if "Test statistic" in lines]
					chi_sq = (float(y[-1].split("    ")[4]))

					red_chi_sq = numpy.round(chi_sq/dof , 2)
					model_dict[m] = red_chi_sq
					#print('Reduced Chi Squared for %s model is'%m, red_chi_sq)
			else:
				continue

		print(model_dict)

		#### sort models by ascending order of reduced chi squared
		model_sorted = dict(sorted(model_dict.items(), key=lambda item: item[1]))

		#### Find best fit model
		i=1
		current_best_val = list(model_sorted.values())[0]
		difference = abs(1 - current_best_val)
		best_fit_mod = list(model_sorted.keys())[0]
		best_chi = current_best_val
		while i < len(model_sorted): #gets the value of the key, value pair from the sorted dictionary
			val = list(model_sorted.values())[i]
			if 0.7 < val < 3.5 :
				if abs(1 - val) < difference:
					current_best_val = val
					difference = abs(1 - val)
					#print(val)
					best_fit_mod = list(model_sorted.keys())[i]
					best_chi = list(model_sorted.values())[i]
			i+=1

		print('Best fit model is',best_fit_mod, ' with reduced chi squared of', best_chi )
		#### Read the log file of the best fit model and extract fit params
		with open('%s/%s_%i_%s_log.log'%(qpo_fit_path, f, seglength, best_fit_mod), 'r') as file:
			lines = file.readlines()
			fit_start =[]
			params = []
			errors =[]
			for i, line in enumerate(lines):
				#find the line where the data with the best fit starts. We are looking for the second set
				#The first set is the initialization of the model.
				if "#   1    1   powerlaw   PhoIndex" in line:
					fit_start.append(i)

			start_best_fit_param = fit_start[-1]
			print(start_best_fit_param)

			num_lor = num_lor_dict[best_fit_mod]
			num_param = num_lor * 3
			print(num_lor, num_param)

			end_best_fit_param = start_best_fit_param + num_param + 1

			for i in range(start_best_fit_param, end_best_fit_param+1):
				params.append(lines[i].split()[-3])
				errors.append(lines[i].split()[-1])
				#print(lines[i].split()[-1])

		print("This is the params array: ")
		print(params)
		print("This is the errors array: ")
		print(errors)
		#### Look for QPOs
		qpo = []
		qpo_err = []
		Q = 0
		for i in range(len(params)):
			#print(i+1, params[i])
			if (i+1) % 3 == 0 and i>=7: #ignoring first 2 params as they fit powerlaw
				Q = float(params[i])/float(params[i+1])
				print("Q: ", Q) ##test delete later
				if Q >= 2.0: #only look for peaked components
					if float(params[i]) > 0.1 and float(params[i]) < 64.0:
						print('QPO with Centroid frequency of', params[i])
						print('Q value is', Q)
						qpo.append([ float(params[i]) , float(params[i+1]) , float(params[i+2]) ])
						qpo_err.append([ float(errors[i]) , float(errors[i+1]) , float(errors[i+2]) ])

		signf = 0
		#### Calculate rms and significance of QPO
		for i in range(len(qpo)):
			area, area_err = (qpo_rms(freq1, qpo[i][0], qpo_err[i][0], qpo[i][1], qpo_err[i][1], qpo[i][2], qpo_err[i][2],freq_int))
			print('RMS and error are', area, area_err)
			signf = area / area_err
			print('Significance is',signf)

			data = numpy.column_stack((numpy.round(qpo[i][0],3), numpy.round(qpo_err[i][0],3), numpy.round(qpo[i][0]/qpo[i][1],2),
						numpy.round(area, 2), numpy.round(area_err, 2), numpy.round(signf, 3), numpy.round(best_chi, 2)))
			numpy.savetxt('%s/qpo_%i.txt'%(qpo_fit_path,i),data,delimiter='\t',newline='\n',header='FREQ,FREQ_ERR,Q,RMS,RMS_ERR,SIG,RED_CHI_SQ')
			##create file to save best fit model. You can then open this file and obtain data when logging QPO (in log QPO code)
			erin_add = open("%s/best_model.txt"%qpo_fit_path, "w")
			erin_add.write(best_fit_mod)
			erin_add.close()
			print("wrote to model file to save best fit model")
		df.loc[idx, 'OBSID'] = obsidFolder
		df.loc[idx, 'Best fit model'] = best_fit_mod
		df.loc[idx, 'RCS'] = best_chi
		df.loc[idx, 'Sig'] = signf
		df.loc[idx, 'Qval'] = Q
df.to_pickle("/Users/rohanpunamiya/Dropbox (GaTech)/NS_Data/CygX2/QandSigValuesTable.pkl")