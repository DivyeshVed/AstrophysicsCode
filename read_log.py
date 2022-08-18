import numpy
import re
import glob
from powerspec import *
import sys
import os

#### MAKE SURE TO RUN qpo_fit_code.py BEFORE RUNNING THIS CODE, OTHERWISE THERE WON'T BE ANY LOG FILES FOR THIS CODE TO READ!
# Getting the path of the data
path = '/Users/rohanpunamiya/Desktop/Data'
# Taking the input from the user. THis input is the prnb folder name. 
input = sys.argv[1]
# Getting the second input from the user which is the obsid folder name
input2 = sys.argv[2]
# Getting the obsid and attaching it to the path
obsid = os.path.join(path,input,input2)
print("This is the obsid path: ", obsid)
# Getting the file name that we want to work with
f = '512lc'
seglength = 1024
# If the files created had indices then we would uncomment the lines below, but since there are no files with these, we don't need them to run this code. 
# ind_obs = "", _a, _b, _c, _d...
# ind_obs = "_b"

# Making a list of the model names that we have made. 
models = ['0.5lor','1lor','1.5lor','2lor', '3lor', '4lor']
# Making a dictionary with the names of the models and the indices that you want to store them in in the dictionary. The value on the left of the colon is the key, and the one to the right is the value.
num_lor_dict = {'0.5lor':2, '1lor':3, '1.5lor':4 , '2lor':5 , '3lor':6, '4lor':7}

# Iterating through the empty list of pathnames that are similar to the obsid
for p in glob.glob(obsid):
	# Finding the path that has the qpo_fit folder and finding the ind_obs file in that folder. There is no ind_obs, thus not really sure how this line is going to work. 
	qpo_fit_path = '%s/qpo_fit'%p
	# Creating an empty dictionary. 
	model_dict ={}

	# Creating a power spectrum file in the same qpo_fit folder. 
	ps_file = '%s/%s_fracrms_ps_%i.txt'%(qpo_fit_path,f,seglength)

	# Finding values for the frequency, power and error using a numpy command. Learn more about this command. This command is used to load data from a text file into numpy.
	freq1, pow1, err1 = numpy.genfromtxt('%s'%ps_file,delimiter='\t', unpack=True)
	# Finding the initial frequency by subtracting the first value in the array from the second value. 
	freq_int = freq1[1] - freq1[0]
	print("This is the initial frequency:",freq_int)
	# Iterating through the list of models
	for m in models:
		# Opening the log files with the name as the models. 
		with open('%s/%s_%i_%s_log.log'%(qpo_fit_path, f, seglength, m), 'r') as file:
			# Reading the lines in the log file. 
			lines = file.readlines()

			# Calculate reduced chi squared
			x = [lines for lines in lines if "Null hypothesis" in lines]
			dof = (float(x[-1].split(" ")[7]))

			y = [lines for lines in lines if "Test statistic" in lines]
			chi_sq = (float(y[-1].split(" ")[-8]))

			red_chi_sq = numpy.round(chi_sq/dof , 2)
			# This is adding the reduced chi squared value to the dictionary made above called model_dict. 
			model_dict[m] = red_chi_sq
			print('Reduced Chi Squared for %s model is'%m, red_chi_sq)
	# Printing the entire dictionary that contains all the key pair values for each model and their reduced chi squared value. 
	print(model_dict)
	# Sort model dictionary by ascending order of reduced chi squared
	model_sorted = dict(sorted(model_dict.items(), key=lambda item: item[1]))
	# Find best fit model
	# Creating a variable to keep count. 
	i = 1
	# This is assigning the current best model to the first value form the sorted dictionary. 
	current_best_val = list(model_sorted.values())[0]
	# Finding the difference between the current best and the ideal we want which is a value of 1. 
	difference = abs(1 - current_best_val)
	# Finding the model name of the current best fit. 
	best_fit_mod = list(model_sorted.keys())[0]
	# Assigning the best chi squared value as the value of the current best fit.
	best_chi = current_best_val
	# Gets the value of the key, value pair from the sorted dictionary.
	while i < len(model_sorted):
		# Iterating through the sorted models dictionary. 
		val = list(model_sorted.values())[i]
		# Creating a criterion for the reduced chi-squared value to be between 0.7 and 3.5
		if 0.7 < val < 3.5 :
			# This is comparing the value of the difference between the ideal and the fits, to the difference caluclated above between the ideal and best fit value. 
			if abs(1 - val) < difference:
				# This then assigns the best fit value to the current_best_val variable. 
				current_best_val = val
				# Finding the difference between the ideal and the current_best_val
				difference = abs(1 - val)
				# Finding the best fit model from the dictionary. 
				best_fit_mod = list(model_sorted.keys())[i]
				# Finding the best fit chi_squared values from the dictionary. 
				best_chi = list(model_sorted.values())[i]
		# Incrementing the iterating variable. 
		i+=1
	# Printing a statement that tells you the best fit model and the reduced chi squared value of the model. 
	print('Best fit mode is',best_fit_mod, ' with reduced chi squared of', best_chi )

	# I THINK THIS IS THE MAIN PURPOSE OF THIS CODE. 
	# Read the log file of the best fit model and extract fit params
	# Opening the log file of the best fit model. 
	with open('%s/%s_%i_%s_log.log'%(qpo_fit_path, f, seglength, best_fit_mod), 'r') as file:
		print("The following log file is open:",file)
		# Reading through all the lines in the file. 
		lines = file.readlines()
		# Creating an empty array to hold the start or inital values that we give xpsec to fit the model.
		fit_start_lines =[]
		# Finding the parameters that are used by xspec to fit the model.
		params = []
		# Finding the errors associated with each of the parameters. 
		errors =[]
		# This keep track of the number of iterations, thus telling us the number of lines. It basically counts the number of iterations. 
		for i, line in enumerate(lines):
			print("This is the value os i: ",i)
			# Finding the line where the data with the best fit starts.
			if "#   1    1   powerlaw   PhoIndex" in line:
				# Adding these values to the array called fit_start. fit_start holds the line numbers where the fitting parameters begin.
				fit_start_lines.append(i)
			print("The fitting parameters begin at these line numbers in the log file:",fit_start_lines)

		# Finding the line that the best fit parameters begin at in the log file.
		start_best_fit_param_lines = fit_start_lines[-1]
		print("This is the line that the best fit parameters being at: ",start_best_fit_param_lines)

		# num_lor refers to the key value of the best fit model in the dictionary that is made on line 28
		num_lor = num_lor_dict[best_fit_mod]
		# num_param refers to the total number of parameters that are outputed in the fitting. It multiplies it by 3 as there are three parameters used to design each lorentzian.
		num_param = num_lor * 3
		# Printing the best fit model and the number of parameters needed to fit the model
		print("This is the key of the lorenztian model that is of best fit:", num_lor)
		print("This is the number of parameters that are used to fit the best fit lorentzian model:",num_param)

		# Finding the last line of the best fit parameters
		end_best_fit_param_line = start_best_fit_param_lines + num_param
		print("This is the last line number of the best fit parameters:",end_best_fit_param_line)

		for i in range(start_best_fit_param_lines, end_best_fit_param_line):
			print("This is the value of i: ",i)
			params.append(lines[i].split()[-3])
			errors.append(lines[i].split()[-1])
			#print(lines[i].split()[-1])

	#### Look for QPOs
	qpo = []
	qpo_err = []
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

	print("QPO:", qpo) ##test delete later
	print(qpo[0])
	print(qpo_err[0])


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
