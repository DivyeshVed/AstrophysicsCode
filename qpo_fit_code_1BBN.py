import numpy
from powerspec import *
import pandas as pd
import subprocess
import os
import glob
import pickle
from os.path import exists
import sys

###
# There is one thing that needs ot be understood before reading this code. Each model that is made here will contain a minimum of one lorenztian. 
# This is because the first lorenztian is always used to model the background noise. Thus the minimum number of lorentzians that one can have
# is two in a model. Models with more than 2 are created and inlcuded in this script too. This script goes up to 6 lorentzians, allowing for 5 features
# to be modeled. 

########
# This code calculates the powspec with frac rms normalization,
# then runs the flx2xsp routine to be able to read the powsepctrum into XSPEC.
# It then produces the inital fit params to load into XSPEC and fits three different models.
# Make sure heainit is running in the terminal window before running this code.
########

# Initialing varibales. Defining the main path that leads the data folder in desktop.
path = '/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/'
# Taking the input from the user. THis input is the prnb folder name. 
input = sys.argv[1]
# Creating the final prnb path
prnb = path + input
# Getting the second input from the user which is the obsid folder name
input2 = sys.argv[2]
# Making the path to the obsid folder
obsid = prnb + "/" + input2
# Making the suffix
suf = ""
# Makinf the lc file name
f = '512lc%s'%suf
# Assigning the seglength
seglength = 1024
# Taking a second user input. Storing this input as integer. 
start_qpo_freq = int(sys.argv[3])
# Creating the models that will look for the QPOs at particular frequencies. 
oneHalf_harmonic_freq = start_qpo_freq * 1.5
start_harmonic = start_qpo_freq * 2.0
start_4har = start_qpo_freq * 4.0
start_subharmonic = start_qpo_freq * 0.5

#Making a folder at the path given
for p in glob.glob(obsid):
	qpo_fit_path = '%s/qpo_fit%s'%(p, suf)
	print(qpo_fit_path)

	#### Read input fits file
	#### This can take a while, so if you are rerunning on a folder where this has been done, comment it out.
	#readfits(infile)

	#### Create a new subdirectory to put all the files relevant to qpo fitting in,
	#### so it doesn't interfere with the bispectrum files
	#### this way, it is also easy to locate
	os.mkdir(qpo_fit_path) # Making the folder at the path

	#### Calculate power spectrum (fractional rms normalization) and save file
	filepath = '%s/%s'%(p, f)
	freq1, power1, pow_err1 = powerspec(filepath, seglength, norm='frac_rms') # Calculating the power spectrum
	data = numpy.column_stack((freq1,power1,pow_err1))
	numpy.savetxt('%s/%s_fracrms_ps_%i.txt'%(qpo_fit_path,f,seglength),data,delimiter='\t',newline='\n',header='FREQUENCY,POWER,ERROR')

	#### might need to play around with the rebin factor. Reduce the noise of the higher frequencies.
	fmin, fmax, freq, power, power_err = log_rebin(freq1, power1, pow_err1, 1.02)
	f_binsize = numpy.array(fmax) - numpy.array(fmin)

	#### Multiplying power and error by the binsize since XSPEC normalises by dividing by the bin size.
	data = numpy.column_stack((numpy.array(fmin), numpy.array(fmax), numpy.array(power)*f_binsize, numpy.array(power_err)*f_binsize))
	numpy.savetxt('%s/%s_%i_rb_ps.txt'%(qpo_fit_path,f,seglength), data)

	#### Move into the subdirectory that we just created above. Puts all files relates to the fitting in this directory.
	os.chdir(qpo_fit_path)

	#### Use flx2xsp to get powerspectrum in correct formats to feed into XSPEC - used to generate the .pha and .rsp files in order for XSPEC to work
	#### Documentation for flx2xsp here:
	#### https://casdc.china-vo.org/mirror/AstroSoft/HEASoft/lheasoft6.10/source/ftools/heasarc/src/flx2xsp/flx2xsp.txt
	#This is a Heasoft command
	subprocess.Popen(["flx2xsp", "%s_%i_rb_ps.txt"%(f,seglength),"%s_%i_rb_ps.pha"%(f,seglength), "%s_%i_rb_ps.rsp"%(f,seglength), "nspec=1", "clobber=yes"])

	# subprocess.call(['./run_flx2xsp.sh', infile, str(seglength), str(path)])

	# Making a model theat uses one power law and two lorentzian.
	# One lorentzian for the Background Noise, one for the QPO. 
	with open('xspec_1lor_fit.sh', 'w') as file:
		file.write('data %s_%i_rb_ps.pha \n'%(f,seglength))
		file.write('setplot energy \n') #1 to 1 relation with frequency
		file.write('ignore **-1e-3 \n') #might need to alter this based on shape of power spectrum
		file.write('log %s_%i_1lor_log.log \n'%(f,seglength))
		# PL +  QPO
		file.write('mo pow+lorentz+lorentz' +
				 '& -1e-3 & 2e-4 & 1e-22 -1 & 0.5 & 1e-3'+ 
				 '%i & 1 & 1e-03 \n'%start_qpo_freq)

		#file.write('newpar 9 = p6 * 2.0 \n')
		file.write('fit 500 \n')
		file.write('chain burn 2000 \n')
		file.write('chain walkers 1000 \n')
		file.write('chain length 10000 \n')
		file.write('chain run 1lor_chain.fits \n')
		file.write('y \n')
		file.write('error 1. 3 4 5 \n')
		file.write('error 1. 6 7 8 \n')
		file.write('error 1. 9 10 11 \n')
		file.write('save model 1lor_model.xcm \n')
		file.write('y \n')
		file.write('cpd device /xw \n')
		file.write('iplo ldata resid model \n')
		file.write('r x3 0.11 64 \n')
		file.write('hardcopy %s_1lor.eps/ps \n'%f)
		file.write('exit \n')
		file.write('exit \n')

# Making a model that uses one power law and three lorenztians.
# One lorenztian for the Background Noise, one for the subharmonic, and one for the QPO.
	with open('xspec_0.5lor_fit.sh', 'w') as file:
		file.write('data %s_%i_rb_ps.pha \n'%(f,seglength))
		file.write('setplot energy \n') #1 to 1 relation with frequency
		file.write('ignore **-1e-3 \n') #might need to alter this based on shape of power spectrum
		file.write('log %s_%i_0.5lor_log.log \n'%(f,seglength))
		# PL +  QPO
		file.write('mo pow+lorentz+lorentz+lorentz' +
							'& 1e-22 -1 & 0.5 & 1e-3 & -1e-3 & 2e-4 &' +
							'& %i & 0.5 & 1e-3'%start_subharmonic+
							'& %i & 0.5 & 1e-3 \n'% start_qpo_freq)


		#file.write('newpar 9 = p6 * 2.0 \n')
		file.write('fit 500 \n')
		file.write('chain burn 2000 \n')
		file.write('chain walkers 1000 \n')
		file.write('chain length 10000 \n')
		file.write('chain run 0.5lor_chain.fits \n')
		file.write('y \n')
		file.write('error 1. 3 4 5 \n')
		file.write('error 1. 6 7 8 \n')
		file.write('error 1. 9 10 11 \n')
		file.write('save model 0.5lor_model.xcm \n')
		file.write('y \n')
		file.write('cpd device /xw \n')
		file.write('iplo ldata resid model \n')
		file.write('r x3 0.11 64 \n')
		file.write('hardcopy %s_0.5lor.eps/ps \n'%f)
		file.write('exit \n')
		file.write('exit \n')
	
	# Making a model with one power law and 3 lorentzians.
	# One lorenztian for the Background Noise, one for the QPO, and one for the 1.5 harmonic.
	with open('xspec_1.5lor_fit.sh', 'w') as file:
		file.write('data %s_%i_rb_ps.pha \n'%(f,seglength))
		file.write('setplot energy \n') #1 to 1 relation with frequency
		file.write('ignore **-1e-3 \n') #might need to alter this based on shape of power spectrum
		file.write('log %s_%i_1.5lor_log.log \n'%(f,seglength))
		# PL +  QPO
		file.write('mo pow+lorentz+lorentz+lorentz' +
							'& 1e-22 -1 & 0.5 & 1e-3 & -1e-3 & 2e-4 &' +
							'& %i & 0.5 & 1e-3'%start_qpo_freq+
							'& %i & 0.5 & 1e-3 \n'% oneHalf_harmonic_freq)


		#file.write('newpar 9 = p6 * 2.0 \n')
		file.write('fit 500 \n')
		file.write('chain burn 2000 \n')
		file.write('chain walkers 1000 \n')
		file.write('chain length 10000 \n')
		file.write('chain run 1.5lor_chain.fits \n')
		file.write('y \n')
		file.write('error 1. 3 4 5 \n')
		file.write('error 1. 6 7 8 \n')
		file.write('error 1. 9 10 11 \n')
		file.write('save model 1.5lor_model.xcm \n')
		file.write('y \n')
		file.write('cpd device /xw \n')
		file.write('iplo ldata resid model \n')
		file.write('r x3 0.11 64 \n')
		file.write('hardcopy %s_1.5lor.eps/ps \n'%f)
		file.write('exit \n')
		file.write('exit \n')

	
	# Making a model with one power law and 3 lorenztians. 
	# One lorentzian for the Background Noise, one for the QPO, one for the harmonic. 
	with open('xspec_2lor_fit.sh', 'w') as file:
		file.write('data %s_%i_rb_ps.pha \n'%(f,seglength))
		file.write('setplot energy \n') #1 to 1 relation with frequency
		file.write('ignore **-1e-3 \n') #might need to alter this based on shape of power spectrum
		file.write('log %s_%i_2lor_log.log \n'%(f,seglength))
		file.write('mo pow+lorentz+lorentz+lorentz' +
							'& -1e-3 & 2e-4 & 1e-22 -1 & 0.5 & 1e-3' +
							'& %i & 0.5 & 1e-3'%start_qpo_freq+
							'& %i & 0.5 & 1e-3 \n'%start_harmonic)
		file.write('fit 500 \n')
		file.write('chain burn 2000 \n')
		file.write('chain walkers 1000 \n')
		file.write('chain length 10000 \n')
		file.write('chain run 2lor_chain.fits \n')
		file.write('y \n')
		file.write('error 1. 3 4 5 \n')
		file.write('error 1. 6 7 8 \n')
		file.write('error 1. 9 10 11 \n')
		file.write('save model 2lor_model.xcm \n')
		file.write('y \n')
		file.write('cpd device /xw \n')
		file.write('iplo ldata resid model \n')
		file.write('r x3 0.11 64 \n')
		file.write('hardcopy %s_2lor.eps/ps \n'%f)
		file.write('exit \n')
		file.write('exit \n')

	# Making a model with one power law and 4 lorentzians. 
	# One lorentzian for the Background noise, one for the subharmonic, one for the QPQ, one for the harmonic. 
	with open('xspec_3lor_fit.sh', 'w') as file:
		file.write('data %s_%i_rb_ps.pha \n'%(f,seglength))
		file.write('setplot energy \n')
		file.write('ignore **-1e-3 \n') #might need to alter this based on shape of power spectrum
		file.write('log %s_%i_3lor_log.log \n'%(f,seglength))
		file.write('mo pow+lorentz+lorentz+lorentz+lorentz' +
							'& -1e-3 & 2e-4 & 1e-22 -1 & 0.5 & 1e-3' +
							'& %i & 0.5 & 1e-3'%start_subharmonic +
							'& %i & 0.5 & 1e-3'%start_qpo_freq+
							'& %i & 0.5 & 1e-3 \n'%start_harmonic)

		#file.write('newpar 9 = p6 * 2.0 \n')
		file.write('fit 500 \n')
		file.write('chain burn 2000 \n')
		file.write('chain walkers 1000 \n')
		file.write('chain length 10000 \n')
		file.write('chain run 3lor_chain.fits \n')
		file.write('y \n')
		file.write('error 1. 3 4 5 \n')
		file.write('error 1. 6 7 8 \n')
		file.write('error 1. 9 10 11 \n')
		file.write('error 1. 12 13 14 \n')
		file.write('save model 3lor_model.xcm \n')
		file.write('y \n')
		file.write('cpd device /xw \n')
		file.write('iplo ldata resid model \n')
		file.write('r x3 0.11 64 \n')
		file.write('hardcopy %s_3lor.eps/ps \n'%f)
		file.write('exit \n')
		file.write('exit \n')

	# Making a model with one power law and 5 lorentzians.
	# One lorentzian for the Background Noise, one for the subharmonic, one for the QPo, one for the harmonic, and one for the 4th harmonic. 
	with open('xspec_4lor_fit.sh', 'w') as file:
		file.write('data %s_%i_rb_ps.pha \n'%(f,seglength))
		file.write('setplot energy \n')
		file.write('ignore **-1e-3 \n') #might need to alter this based on shape of power spectrum
		file.write('log %s_%i_4lor_log.log \n'%(f,seglength))

		file.write('mo pow+lorentz+lorentz+lorentz+lorentz+lorentz'+
							'& -1e-3 & 2e-4 & 1e-22 -1 & 0.5 & 1e-3' +
							'& %i & 0.5 & 1e-3 & %i & 0.5 & 1e-3'%(start_subharmonic,start_qpo_freq) +
							'& %i & 0.5 & 1e-3 & %i & 0.5 & 1e-3 \n'%(start_harmonic,start_4har))

		#file.write('newpar 9 = p6 * 2.0 \n')
		file.write('fit 500 \n')
		file.write('chain burn 2000 \n')
		file.write('chain walkers 1000 \n')
		file.write('chain length 10000 \n')
		file.write('chain run 4lor_chain.fits \n')
		file.write('y \n')
		file.write('error 1. 3 4 5 \n')
		file.write('error 1. 6 7 8 \n')
		file.write('error 1. 9 10 11 \n')
		file.write('error 1. 12 13 14 \n')
		file.write('error 1. 15 16 17 \n')
		file.write('save model 4lor_model.xcm \n')
		file.write('y \n')
		file.write('cpd device /xw \n')
		file.write('iplo ldata resid model \n')
		file.write('r x3 0.11 64 \n')
		file.write('hardcopy %s_4lor.eps/ps \n'%f)
		file.write('exit \n')
		file.write('exit \n')

	#### Run XSPEC and feed it the particular scripts
	proc = subprocess.Popen(["xspec < xspec_1lor_fit.sh"], shell=True)
	proc.communicate() # Print to the terminal

	proc = subprocess.Popen(["xspec < xspec_0.5lor_fit.sh"], shell=True)
	proc.communicate() # Print to the terminal
	
	proc = subprocess.Popen(["xspec < xspec_1.5lor_fit.sh"], shell=True)
	proc.communicate() # Print to the terminal

	proc = subprocess.Popen(["xspec < xspec_2lor_fit.sh"], shell=True)
	proc.communicate() # Print to the terminal

	proc = subprocess.Popen(["xspec < xspec_3lor_fit.sh"], shell=True)
	proc.communicate()

	proc = subprocess.Popen(["xspec < xspec_4lor_fit.sh"], shell=True)
	proc.communicate()

	print("DONE WITH FITTING!")

	models = ['1lor','0.5lor','1.5lor','2lor', '3lor', '4lor']
	model_dict ={}

	for m in models:
		with open('%s/%s_%i_%s_log.log'%(qpo_fit_path, f, seglength, m), 'r') as filelog:
			lines = filelog.readlines()

			#### Calculate reduced chi squared. Telling us how good of a fit it is.
			x = [lines for lines in lines if "Null hypothesis" in lines]
			dof = (float(x[-1].split(" ")[7]))

			y = [lines for lines in lines if "Test statistic" in lines]
			chi_sq = (float(y[-1].split(" ")[-8]))

			red_chi_sq = numpy.round(chi_sq/dof , 1)
			model_dict[m] = red_chi_sq
			print('Reduced Chi Squared for %s model is'%m, red_chi_sq)


	print(model_dict)
	os.chdir(path)

# # # Checking if the qpo_fit folder has been produced and updating pkl file
# # Loading the pkl file.
# data = pickle.load(open("/Users/rohanpunamiya/Desktop/AstrophysicsCode/dataTable.pkl","rb"))
# # Getting the names of all the obsids inside the prnb folder
# list_of_obsid = os.listdir(prnb)
# # Checking the list if there is a item with a particular name
# if '.DS_Store' in list_of_obsid:
#     # Deleting it if that item exists.
#     list_of_obsid.remove('.DS_Store')
# # Iterating through the list of obsids
# for item in list_of_obsid:
# 	# Going into the obsid directory
# 	os.chdir(prnb + "/" + item)
# 	# Checking for the qpo_fit folder
# 	qpo_fit__exists = exists('qpo_fit')
# 	# If qpo_fit folder exists, then change the column under qpo_fit_code.py to yes
# 	if qpo_fit__exists == True:
# 		# Finding the index of the obsid in the dataframe
# 		idx = int(data[data["OBSID"]== str(item)].index.values)
# 		# Replacing the qpo_fit_code.py column to yes at the particular row index
# 		data.loc[idx,'Ran qpo_fit_code.py'] = 'Yes'
# data.to_pickle("/Users/rohanpunamiya/Desktop/AstrophysicsCode/dataTable.pkl")

### Once this code is run, run read_log.py to extract the values of the qpo from the logs produced by XSPEC
