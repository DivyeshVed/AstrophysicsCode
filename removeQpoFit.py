# This code checks if the qpo_fit folder exists, and if it does, it deletes the folder. 
import sys 
import os
from os.path import exists
import shutil
import pickle 

data = pickle.load(open("/Users/rohanpunamiya/Dropbox (GaTech)/NS_Data/CygX2/frequencyTable.pkl","rb"))
for idx in data.index:
    input = data["PRNB"][idx]
    input2 = data["OBSID"][idx]
    # Initializing the path.
    path = '/Users/rohanpunamiya/Dropbox (GaTech)/NS_Data/CygX2/'
    obsid = path + "/" + input + "/" + input2
    os.chdir(obsid)
    # Confirming that we have got into the obsid folder successfully
    print('Got into the OBSID folder')
    # Checking for the qpo_fit folder in the obsid folder
    qpo_fit__exists = exists('qpo_fit')
    # If qpo_fit folder exists, then delete the folder and inform the user that folder once existed, but has now been deleted. 
    if qpo_fit__exists == True:
        print('The QPO Fit folder exsits...')
        shutil.rmtree(obsid + "/qpo_fit")
        print('Deleted the QPO Fit folder!')
    else:
        # If the folder did not exist in the first place, then inform the user that the folder doesn't exist. 
        print("The QPO Fit folder does not exist in this obsid")