# This file is used to open all the eps files to check whether the fitting is right. 
import os
import sys
import numpy
import time
import pickle
import tkinter
import subprocess
import time

# Loading the pkl file.
data = pickle.load(open("/Users/rohanpunamiya/Desktop/AstrophysicsCode/dataTable.pkl","rb"))
# print(data.to_string())

# Defining the main path that leads the data folder in desktop.
path = '/Users/rohanpunamiya/Desktop/Data/'
# Taking the input from the user. This input is the prnb folder name. 
input = sys.argv[1]
# Creating the final prnb path.
prnb = path + input
# Listing all the obsids inside the prnb folder.
listOfObsids = os.listdir(prnb)
# Checking the list if there is a item with a particular name
if '.DS_Store' in listOfObsids:
    # Deleting it if that item exists.
    listOfObsids.remove('.DS_Store')
# The file extension that we are loooking for for the fit
fileExtension = '.eps'
# The file extension that we are looking for while calculating reduced chi squared value
fileExtension2 = '.log'
# Creating an empty list
epsFilesList = []
# Creating an empty list to store the model numbers
modelNumberList = []
# Creating an empty list to store the reduced chi sqaured values
rcsList = []
# Creating iterating vairbale
i = 0
# Iterating through the listOfObsids
for obsid in listOfObsids:
    print("The obsid seen is: ", obsid)
    # Opening the qpo_fit folder in the obsid folder
    qpoFitFolderPath = os.path.join(prnb,obsid,"qpo_fit")
    # Change the wokring directory to the qpo_fit folder in the obsid folder
    os.chdir(qpoFitFolderPath)
    # Iterating through every file in the qpoFitFolderPath and looking for the file with the eps extension.
    for file in os.listdir(qpoFitFolderPath):
        # If the file has the eps extension
        if file.endswith(fileExtension):
            # Open the eps file
            os.system("open " + file)
        elif file.endswith(fileExtension2):
            # Finding the model number
            if file[12] == ".":
                modelNumber = file[11:14]
            else:
                modelNumber = file[11]
            modelNumberList.append(modelNumber)
            # Opening the log file
            with open(file) as logFile: 
                # Reading the lines in the log file.
                lines = logFile.readlines()
			    # Calculate reduced chi squared
                x = [lines for lines in lines if "Null hypothesis" in lines]
                dof = (float(x[-1].split(" ")[7]))
            
                y = [lines for lines in lines if "Test statistic" in lines]
                chi_sq = (float(y[-1].split(" ")[-8]))
                red_chi_sq = numpy.round(chi_sq/dof , 2)
                print('Reduced Chi Squared for', modelNumber,'lorenztian model is:', red_chi_sq)
                # Finding the index of the obsid in the dataframe
                idx = int(data[data["OBSID"]== str(obsid)].index.values)
	            # Replacing the qpo_fit_code.py column to yes at the particular row index
                data.loc[idx,modelNumber + ' lor model'] = red_chi_sq
    # Create a tkinter root window
    root = tkinter.Tk()
    # Root window title and dimension
    root.title("When you press a button the message will pop up")
    root.geometry('200x100')
    # Create a messagebox showinfo
    def onClick():
        root.destroy()
        subprocess.call(['osascript', '-e', 'tell application "Preview" to quit'])
        time.sleep(3)
    # Create a Button
    button = Button(root, text="Next obsid", command=onClick, height=2, width=10)
    # Set the position of button on the top of window.
    button.pack(side='bottom')
    root.mainloop()

# Saving the pandas table
data.to_pickle("/Users/rohanpunamiya/Desktop/AstrophysicsCode/dataTable.pkl")
