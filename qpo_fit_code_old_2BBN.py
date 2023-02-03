import numpy
from powerspec import *
import pandas as pd
import subprocess
import os
import glob
import sys
import pickle
import time

########
# This code calculates the powspec with frac rms normalization,
# then runs the flx2xsp routine to be able to read the powsepctrum into XSPEC.
# It then produces the inital fit params to load into XSPEC and fits three different models.
# Make sure heainit is running in the terminal window before running this code.
########

data = pickle.load(open("/Users/rohanpunamiya/Dropbox (GaTech)/NS_Data/CygX2/frequencyTable.pkl","rb"))
print("Data has been loaded")
for idx in range(len(data)):
	data = pickle.load(open("/Users/rohanpunamiya/Dropbox (GaTech)/NS_Data/CygX2/frequencyTable.pkl","rb"))
	input = data["PRNB"][idx]
	print("This is the index from the table: " + str(idx))
	input2 = data["OBSID"][idx]
	# Initialing varibales. Defining the main path that leads the data folder in desktop.
	path = '/Users/rohanpunamiya/Dropbox (GaTech)/NS_Data/CygX2'
	obsid = path + "/" + input + "/" + input2
	start_qpo_freq = data["Frequency"][idx]
	if start_qpo_freq == "DNE" or os.path.exists(obsid + "/qpo_fit"):
		continue
	else: 
		suf = ''
		f = '512lc%s'%suf
		seglength = 1024
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

			#### reate a new subdirectory to put all the files relevant to qpo fitting in,
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
			#THis is a Heasoft command
			subprocess.Popen(["flx2xsp", "%s_%i_rb_ps.txt"%(f,seglength),"%s_%i_rb_ps.pha"%(f,seglength), "%s_%i_rb_ps.rsp"%(f,seglength), "nspec=1", "clobber=yes"])

			#subprocess.call(['./run_flx2xsp.sh', infile, str(seglength), str(path)])

			#Writing the script of XSPEC Commands that we will feed to XSPEC.
			with open('xspec_3lor_fit.sh', 'w') as file:
				file.write('data %s_%i_rb_ps.pha \n'%(f,seglength))
				file.write('setplot energy \n')
				file.write('ignore **-1e-3 \n') #might need to alter this based on shape of power spectrum
				file.write('log %s_%i_3lor_log.log \n'%(f,seglength))
				# PL + BBN + BBN2 +  QPO + Harmonic
				file.write('mo pow+lorentz+lorentz+lorentz+lorentz' +
									'& -1e-3 & 2e-4 & 1e-22 -1 & 0.5 & 1e-3' +
									'& 1e-22 -1 & 1.0 & 1e-3' +
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
				file.write('save model 3lor_model.xcm \n')
				file.write('y \n')
				file.write('cpd device /xw \n')
				file.write('iplo ldata resid model \n')
				file.write('r x3 0.11 64 \n')
				file.write('hardcopy %s_3lor.eps/ps \n'%f)
				file.write('exit \n')
				file.write('exit \n')

			with open('xspec_4lor_fit.sh', 'w') as file:
				file.write('data %s_%i_rb_ps.pha \n'%(f,seglength))
				file.write('setplot energy \n')
				file.write('ignore **-1e-3 \n') #might need to alter this based on shape of power spectrum
				file.write('log %s_%i_4lor_log.log \n'%(f,seglength))

				# PL + BBN +BBN2 + subharmonic + QPO + Harmonic
				file.write('mo pow+lorentz+lorentz+lorentz+lorentz+lorentz'+
									'& -1e-3 & 2e-4 & 1e-22 -1 & 0.5 & 1e-3' +
									'& 1e-22 -1 & 1.0 & 1e-3' +
									'& %i & 0.5 & 1e-3 & %i & 0.2 & 1e-2'%(start_subharmonic,start_qpo_freq) +
									'& %i & 0.5 & 1e-3 \n'%start_harmonic)


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
				file.write('save model 4lor_model.xcm \n')
				file.write('y \n')
				file.write('cpd device /xw \n')
				file.write('iplo ldata resid model \n')
				file.write('r x3 0.11 64 \n')
				file.write('hardcopy %s_4lor.eps/ps \n'%f)
				file.write('exit \n')
				file.write('exit \n')

			#### Might need to add another model here
			#### PL + BBN + QPO + Harmonic + 4th harmonic


			with open('xspec_5lor_fit.sh', 'w') as file:
				file.write('data %s_%i_rb_ps.pha \n'%(f,seglength))
				file.write('setplot energy \n')
				file.write('ignore **-1e-3 \n') #might need to alter this based on shape of power spectrum
				file.write('log %s_%i_5lor_log.log \n'%(f,seglength))

				# PL + BBN + BBN2 + QPO + subharmonic + Harmonic + 4th harmonic
				file.write('mo pow+lorentz+lorentz+lorentz+lorentz+lorentz+lorentz' +
									'& -1e-3 & 2e-4 & 1e-22 -1 & 0.5 & 1e-3 & 1e-22 -1 & 1.0 & 1e-3' +
									'& %i & 0.5 & 2e-4 & %i & 0.2 & 1e-3'%(start_subharmonic, start_qpo_freq) +
									' & %i & 0.5 & 1e-3 & %i & 0.5 & 1e-3 \n'%(start_harmonic, start_4har))

				#file.write('newpar 9 = p6 * 2.0 \n')
				file.write('fit 500 \n')
				file.write('chain burn 2000 \n')
				file.write('chain walkers 1000 \n')
				file.write('chain length 10000 \n')
				file.write('chain run 5lor_chain.fits \n')
				file.write('y \n')
				file.write('error 1. 3 4 5 \n')
				file.write('error 1. 6 7 8 \n')
				file.write('error 1. 9 10 11 \n')
				file.write('error 1. 12 13 14 \n')
				file.write('error 1. 15 16 17 \n')
				file.write('save model 5lor_model.xcm \n')
				file.write('y \n')
				file.write('cpd device /xw \n')
				file.write('iplo ldata resid model \n')
				file.write('r x3 0.11 64 \n')
				file.write('hardcopy %s_5lor.eps/ps \n'%f)
				file.write('exit \n')
				file.write('exit \n')

			#### Run XSPEC and feed it the particular scripts
			proc = subprocess.Popen(["xspec < xspec_3lor_fit.sh"], shell=True)
			try:
				proc.communicate(timeout = 500) # Print to the terminal
			except subprocess.TimeoutExpired:
				proc.kill()
				continue

			proc = subprocess.Popen(["xspec < xspec_4lor_fit.sh"], shell=True)
			try:
				proc.communicate(timeout = 500) # Print to the terminal
			except subprocess.TimeoutExpired:
				proc.kill()
				continue

			proc = subprocess.Popen(["xspec < xspec_5lor_fit.sh"], shell=True)
			try:
				proc.communicate(timeout = 500) # Print to the terminal
			except subprocess.TimeoutExpired:
				proc.kill()
				continue


			print("DONE WITH FITTING!")

			models = ['3lor', '4lor', '5lor']
			model_dict ={}

			for m in models:
				with open('%s/%s_%i_%s_log.log'%(qpo_fit_path, f, seglength, m), 'r') as filelog:
					lines = filelog.readlines()

					#### Calculate reduced chi squared. Telling us how good of a fit it is.
					x = [lines for lines in lines if "Null hypothesis" in lines]
					dof = (float(x[-1].split(" ")[7]))

					y = [lines for lines in lines if "Test statistic" in lines]
					chi_sq = (float(y[-1].split("    ")[4]))

					red_chi_sq = numpy.round(chi_sq/dof , 1)
					model_dict[m] = red_chi_sq
					print('Reduced Chi Squared for %s model is'%m, red_chi_sq)
			
			print(model_dict)
		
#### Once this code is run, run read_log.py to extract the values of the qpo from the logs produced by XSPEC
