# import pandas as pd

# #Creating a dataframe with the desired column names
column_names = ['Target Name', 'Status', 'prnb', 'OBSID', 'Ran extract.py', 'Ran analyse.py', 'QPO Present', 'QPo Frequency (Hz)']
df = pd.DataFrame(columns = column_names)

# numObservations = 582
# for i in range(numObservations):
#     df.at[i, 'OBSID'] = 70104

# print(df)
from extractingLines import *
fileOpener("downloadCodes.txt","allCodes.txt")