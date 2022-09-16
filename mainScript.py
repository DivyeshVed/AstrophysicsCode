# This is the main script file. Want to make it such that only this file is called, and it runs all the code in extract, analyse and qpo_fit_code. 
import sys
import os
from extract import *
from analyse import * 
import pandas as pd
from postDownload import *

# Taking the first input from the user that will be the prnb number
prnbFolder = sys.argv[1]
# Creating the universal path to the prnb folder
# prnbPath = '/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/%s' %prnbFolder
prnbPath = '/Users/rohanpunamiya/Documents/%s' %prnbFolder
# Making a list of all the obsids in the prnb folder
obsidList = os.listdir(prnbPath)
# Constructing the path to all the propids.
obsidsPath = prnbPath + '/*'
# Creating the dataframe. 
# Making a list of all the names that we want as column headers for the table. 
column_names = ['Target Name', 'Status', 'prnb', 'OBSID', 'Ran extract.py', 'Ran analyse.py', 'QPO Present', 'QPO Frequency (Hz)']
# Creating the dataframe with the column headers.
df = pd.DataFrame(columns = column_names)
# Saving the dataframe that we just created.
# df.to_pickle("/Users/rohanpunamiya/Desktop/AstrophysicsCode/downloadingData/newDataFrame.pkl")
df.to_pickle("/Users/rohanpunamiya/Documents/testDataFrame.pkl")
# Calling the postDownload function
postDownload()
# Calling the function that will run the code in extract
extract(prnbPath,obsidList,obsidsPath)
# Calling the function that will run the code in analyse
analyse(prnbPath,obsidList,obsidsPath)


