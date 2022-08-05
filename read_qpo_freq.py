import numpy
import pandas as pd
import glob
import os

####
# Code to read the qpo values after the fitting routine has been run.
####

path = '/Users/rohanpunamiya/Desktop/Data'
obsid_path = '%s/P10067/10067-01-01-00'%path
#obsid_path = '%s/P80701/80701-01-26-00'%path

suf_num = [0,1,2,3,4]
suf_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p']

rows_list=[] #list of dictionaries to turn into dataframe
for p in glob.glob(obsid_path):
	for ind in range(len(suf_list)):
		qpo_fit_path = '%s/qpo_fit_%s'%(p,suf_list[ind])
		if os.path.exists(qpo_fit_path):
			if os.path.isfile('%s/128lc_%s_fracrms_ps_1024.txt'%(qpo_fit_path, suf_list[ind])) or os.path.isfile('%s/128lc_%s_fracrms_ps_2048.txt'%(qpo_fit_path,suf_list[ind])):
				for num in range(len(suf_num)): #for each qpo found by fitting routine
					if os.path.exists('%s/qpo_%i.txt'%(qpo_fit_path,num)):
						string = p.split("/")
						#obsid = string[-1] + suf_list[ind]
						obsid = string[-1]
						f, f_err, q, rms, rms_err, sig, chi = numpy.genfromtxt('%s/qpo_%i.txt'%(qpo_fit_path,num),delimiter='\t', unpack=True)
						if sig >= 3.0: #if qpo is significant
							dict1 = {'OBSID':obsid,'FREQ':f,'FREQ_ERR':f_err,'Q':q,'RMS':rms,'RMS_ERR':rms_err,'SIG':sig,'RED_CHI_SQ':chi}
							rows_list.append(dict1)
		else:
			string = p.split("/")
			obsid = string[-1]
			print('Need to run fit for %s, particularly %s'%(obsid, suf_list[ind]))


#print(rows_list)
df = pd.DataFrame(rows_list)
df.to_pickle('./GRS1915_obsfreq.pkl')


print(df)
