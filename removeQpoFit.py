# This code checks if the qpo_fit folder exists, and if it does, it deletes the folder. 
import sys 
import os
from os.path import exists
import shutil

# Initializing the path.
path = '/Users/rohanpunamiya/Desktop/Data/'
# Taking input from the user. The input is the prnb folder name. 
input = sys.argv[1]
# Combining the path and the prnb folder name to make the prnb folder path. 
prnb = path + input
# Confirming that the path made leads to the right folder. 
print("This is the path to the prnb folder: " + prnb)
# Getting the names of all the obsids inside the prnb folder
list_of_obsid = os.listdir(prnb)
# Checking the list if there is a item with a particular name
if '.DS_Store' in list_of_obsid:
    # Deleting it if that item exists.
    list_of_obsid.remove('.DS_Store')
# Printing the list of obsid
print(list_of_obsid)
# Iterating through the list of obsids
for item in list_of_obsid:
    # Going into the obsid directory
    obsid = prnb + "/" + item
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