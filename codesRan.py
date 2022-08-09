# The idea of this code is to have a pandas table that holds the obsids of the observations, and which codes have been run on the obsid. 

# The first step is to import an excel sheet that contains all the OBSIDs that we have downloaded.
# Importing the numpy module
import numpy as np
# Importing the os module
import os
from os.path import exists
# Importing the pandas library.
import pandas as pd
# Reading the excel sheet and importing it into a pandas table.
df = pd.read_excel('/Users/rohanpunamiya/Desktop/AstrophysicsCode/DownloadedOBSIDS.xls')
# Renaming the column headers in the dataframe
df.columns = ['prnb', 'OBSID', 'Ran extract.py', 'Ran analyse.py', 'Ran qpo_fit_code.py', '0.5 lor model', '1 lor model' , '1.5 lor model', '2 lor model', '3 lor model', '4 lor model', 'Best Fit Model (RCS)']
# Iterating through the rows in the dataframe
for index, row in df.iterrows():
    # Getting the prnb number, so we can access that folder in the Data folder on the desktop
    dataFolderName = "P" + str(df['prnb'][index])
    # Getting the obsid from the table
    obsid = str(df['OBSID'][index])
    # Checking if the prnb folder exists at the location
    prnb_exists = exists('/Users/rohanpunamiya/Desktop/Data/' + dataFolderName)
    # If the prnb exsits, then we go into it the folder
    if prnb_exists == True:
        os.chdir('/Users/rohanpunamiya/Desktop/Data/' + dataFolderName)
        # Now checking if the obsid exists
        obsid_exists = exists('/Users/rohanpunamiya/Desktop/Data/' + dataFolderName + '/' + obsid)
        # If the osbid exsists, then we go into that folder
        if obsid_exists == True:
            os.chdir('/Users/rohanpunamiya/Desktop/Data/' + dataFolderName + '/' + obsid)
            # Now checking if there is a datamode.txt file
            datamode_exists = exists('datamode.txt')
            # Now checking if there is a 5121lc file
            lc_exists = exists('512lc.lc')
            # If datamode exists, then change the column under ran extract.py to yes
            if datamode_exists == True & lc_exists == True:
                df.loc[index,'Ran extract.py'] = 'Yes'
            # Now checking if there is a txt file with a particular name
            txt_exists = exists('512lc.txt')
            # If the txt file exists, then change the column under analyse.py to yes
            if txt_exists == True:
                df.loc[index,'Ran analyse.py'] = 'Yes'
            # Now checking if there is a folder called qpo_fit
            qpo_fit_exists = exists('qpo_fit')
            # If qpo_fit folder exists, then change the column under qpo_fit_code.py to yes
            if qpo_fit_exists == True:
                df.loc[index,'Ran qpo_fit_code.py'] = 'Yes'

print(df.to_string())

# Saving the pandas table as a CSV file in the AstrophysicsCode directory
df.to_pickle('/Users/rohanpunamiya/Desktop/AstrophysicsCode/dataTable.pkl')



    


