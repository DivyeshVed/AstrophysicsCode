import sys
import os 

# Taking input from the user. This input is the prnb folder name. 
prnb = sys.argv[1]
# Getting the path of the data
obsid = '/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/%s' %prnb
# Making a list to store the obsids that do not contain qpo_fit folders
containsQpoFitFolder = []
noQpoFitFolder = []
containsBestModelFile = []
noBestModelFile = []
containsQpoFitFolderCounter = 0
noQpoFitFolderCounter = 0
containsBestModelFileCounter = 0
noBestModelFileCounter = 0
# Making a list of obsids
listOfObsids = os.listdir(obsid)
for obsidFolder in listOfObsids:
    if obsidFolder == ".DS_Store":
        continue
    else: 
        obsidFolderPath = os.path.join(obsid,obsidFolder)
        os.chdir(obsidFolderPath)
        # Checking if the qpo_fit folder exists
        if os.path.exists('qpo_fit'):
            containsQpoFitFolder.append(obsidFolder)
            containsQpoFitFolderCounter += 1
            os.chdir(os.path.join(obsidFolderPath,'qpo_fit'))
            if os.path.exists('best_model.txt'):
                containsBestModelFile.append(obsidFolder)
                containsBestModelFileCounter += 1
            else:
                noBestModelFile.append(obsidFolder)
                noBestModelFileCounter += 1
        else:
            noQpoFitFolder.append(obsidFolder)
            noQpoFitFolderCounter += 1

print("This is a list of obsids that contain the qpo_fit folder:")
print(containsQpoFitFolder)
print("There are " + str(containsQpoFitFolderCounter) + " obsids that contain the qpo_fit folder in this prnb")
print("\n")
print("This is a list of obsids that contain the qpo_fit folder and the best_model.txt file:")
print(containsBestModelFile)
print("There are " + str(containsBestModelFileCounter) + " obsids that contain the qpo_fit folder and best_model.txt file in this prnb")
print("\n")
print("This is a list of obsids that contain the qpo_fit folder but DOES NOT contain the best_model.txt file:")
print(noBestModelFile)
print("There are " + str(noBestModelFileCounter) + " obsids that DO NOT contain the best_model.txt file but containa the qpo_fit folder in this prnb")
print("\n")
print("This is a list of obsids that do not contain the qpo_fit folder:")
print(noQpoFitFolder)
print("There are " + str(noQpoFitFolderCounter) + " obsids that DO NOT contain the qpo_fit folder in this prnb")


