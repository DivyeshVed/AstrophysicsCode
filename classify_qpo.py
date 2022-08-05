import glob
import sys
import re
import pandas as pd
from astropy.io import fits
from os import path
import os.path
import pickle
import numpy

propid = 'P70104/70104-02-02-00'
path = '/Users/erinhorbacz/Downloads/Research/testData/%s'%propid
## suf = _a, _b, _c, _d, or ""
suf = '_b'
infile = '%s/128lc%s'%(path, suf)

classification = "undetermined"
log_qpo = True ##Check Q value; if Q not significant (< 2) do not log!


def append_dataframe(classification):
        with open('%s/qpo_fit%s/compile_dataframe_info.pkl'%(path, suf), 'rb') as f:
        #dict2 = pickle.load(f)
            data = pd.read_pickle(f)
            data["CLASSIFICATION"] = classification
            #updated_data = data.append(df, ignore_index = True)
            print(data)
            data.to_pickle('%s/qpo_fit%s/compile_dataframe_info.pkl'%(path, suf))


##Get freq and integrated rms values for QPO
num_qpo = [0] ##may need to change this number (ex- qpo_fit_1.txt)
for j in range(len(num_qpo)):
    #print('%s/qpo_fit%s/qpo_%i.txt'%(path, suf, j))
    if os.path.exists('%s/qpo_fit%s/qpo_%i.txt'%(path, suf, j)):
        file = open('%s/qpo_fit%s/qpo_%i.txt'%(path, suf, j), 'r')
        lines = file.readlines()
        for i in range(1, len(lines)):
            line = lines[i].split("\t")
            freq = "%.5f"%float(line[0])
            freq = float(freq)
            integrated_rms = "%.5f"%float(line[3])
            integrated_rms = float(integrated_rms) * 100
            file.close()
    else:
        if j == 0:
            print("QPO wasn't significant enough; no file qpo_0.txt found. (REMEMBER: this is only checking qpo_0)")
            quit()
        ##Q not significant (< 2) do not log!
print("FREQ:", freq, "INTEGRATED RMS", integrated_rms)


if (freq >= 0.1) and (freq <= 60):
    if (freq >= 3) and (freq <= 9):
        if (integrated_rms >= 2) and (integrated_rms <= 5):
            classification = "FBO"
            print("Classification:", classification)
    if (freq >= 10) and (freq <= 20):
        if (integrated_rms >= 3) and (integrated_rms <= 10):
            classification = "NBO"
    if (freq >= 20) and (freq <= 30):
        if (integrated_rms >= 3) and (integrated_rms <= 30):
            classification = "HBO"
            print("Classification:", classification)
        if ((integrated_rms >= 3) and (integrated_rms <= 10)) and ((freq >= 20) and (freq <= 25)):
            classification = "NBO"
            print("Classification:", classification)
df = pd.DataFrame({"CLASSIFICATION": classification}, index = [0])
print("Final classification is", classification)
print("Accept this value? ")
response = input("Enter Y or N: ")

##add classification to some document or dataframe
if response == "Y":
    append_dataframe(classification)

else:
    print("Would you like to classify it?")
    act_on_classify = input("Enter Y or N: ")
    if act_on_classify == "Y":
        classification = input("Enter classification: ")
        append_dataframe(classification)
    else:
        print("quitting the program.")
        quit()
