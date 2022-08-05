import pandas as pd

# Creating the dataframe. Need to run this code firstt and then run the rest of the code. 
# Run this first, and then run postDownload.py.
# Making a list of all the names that we want as column headers for the table. 
column_names = ['Target Name', 'Status', 'prnb', 'OBSID', 'Ran extract.py', 'Ran analyse.py', 'QPO Present', 'QPO Frequency (Hz)']
# Creating the dataframe with the column headers.
df = pd.DataFrame(columns = column_names)
# Saving the dataframe that we just created.
df.to_pickle("/Users/rohanpunamiya/Desktop/AstrophysicsCode/downloadingData/newDataFrame.pkl")