import sys
import os
# This file is used to count the number of files in the qpo_fit folder

# Taking input from the user. This input is the prnb folder name. 
prnb = sys.argv[1]
# Getting the path of the data
obsid = '/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/%s' %prnb
# Listing all the obsids inside the prnb folder.
listOfObsids = os.listdir(obsid)
# Checking the list if there is a item with a particular name
if '.DS_Store' in listOfObsids:
    # Deleting it if that item exists.
    listOfObsids.remove('.DS_Store')
for folder in listOfObsids:
    print("The current obsid is: " + folder)
    # Changing the working directory to the obsid
    qpo_fit_path = os.path.join(obsid,folder,"qpo_fit")
    print("we are now in qpo_fit folder")
    count = 0
    print("The count has started")
    # Iterate directory
    for path in os.listdir(qpo_fit_path):
        count += 1
    print('File count:', count)
    if count < 30:
        print("This obsid does not have the eps files in its qpo_fit folder. Ignore this obsid")
