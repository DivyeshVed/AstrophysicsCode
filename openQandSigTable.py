import pickle
import pandas as pd
import sys

# Creating the dataframe. Need to run this code firstt and then run the rest of the code. 
# Run this first, and then run postDownload.py.
# Making a list of all the names that we want as column headers for the table. 
# column_names = ['OBSID',
# 				'Best Fit Model',
# 				'Fund.Freq',
# 				'Fund.FreqEr',
# 				'Fund.RCS',
# 				'Fund.RMS',
# 				'Fund.RMSEr',
# 				'Fund.Q',
# 				'Fund.Sig',
# 				'Harm.Freq',
# 				'Harm.FreqEr',
# 				'Harm.RCS',
# 				'Harm.RMS',
# 				'Harm.RMSEr',
# 				'Harm.Q',
# 				'Harm.Sig']

# column_names = ['OBSID',
# 'Best Fit Model',
# 'Fund.Freq',
# 'Fund.RCS',
# 'Fund.RMS',
# 'Fund.Q',
# 'Fund.Sig',
# 'Harm.Freq',
# 'Harm.RCS',
# 'Harm.RMS',
# 'Harm.Q',
# 'Harm.Sig']
# df = pd.DataFrame(columns = column_names)
# # Saving the dataframe that we just created.
# df.to_pickle('/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/Q_Significance_Values.pkl')

# data = pickle.load(open("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/Q_Significance_Values.pkl","rb"))
# data = data.drop('Best Model Fit',axis = 1)
# data = data.reset_index()
# data = data.drop('index',axis = 1)
# print(data.to_string())
# print("There are",str(len(data)),"obsids in the table")
# data.to_pickle("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/Q_Significance_Values.pkl")

input = sys.argv[1]
data = pickle.load(open("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/Q_Significance_Values.pkl","rb")
if input == "clear": 
    data.drop(data.index,inplace=True)
elif input == 'sort':
    data = data.sort_values(by='OBSID')
elif input == 'reset_index':
    data = data.reset_index()
    data = data.drop('index',axis = 1)
print(data.to_string())
data.to_pickle("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/Q_Significance_Values.pkl")