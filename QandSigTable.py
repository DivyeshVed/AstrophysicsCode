import pickle
import pandas as pd

# Creating the dataframe. Need to run this code firstt and then run the rest of the code. 
# Run this first, and then run postDownload.py.
# Making a list of all the names that we want as column headers for the table. 
# column_names = ['OBSID', 'Q Value', 'Significance']
# # Creating the dataframe with the column headers.
# df = pd.DataFrame(columns = column_names)
# # Saving the dataframe that we just created.
# df.to_pickle('/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/Q_Significance_Values.pkl')

data = pickle.load(open("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/Q_Significance_Values.pkl","rb"))
columnHeader = ['OBSID','Q Value','Significance']
goodValues = pd.DataFrame(columns = columnHeader)
okayValues = pd.DataFrame(columns = columnHeader)
# data.to_pickle("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/Q_Significance_Values.pkl")
for idx in data.index:
    if (data['Q Value'][idx]) == 'DNE':
        data['Q Value'][idx] = 0
    elif float(data['Significance'][idx]) > 3.0:
        if float(data['Q Value'][idx]) >= 2.0:
            goodValues.loc[idx,'OBSID'] = data['OBSID'][idx]
            goodValues.loc[idx,'Q Value'] = data['Q Value'][idx]
            goodValues.loc[idx,'Significance'] = data['Significance'][idx]
        elif (float(data['Q Value'][idx]) >= 1.0 and float(data['Q Value'][idx]) < 2.0):
            okayValues.loc[idx,'OBSID'] = data['OBSID'][idx]
            okayValues.loc[idx,'Q Value'] = data['Q Value'][idx]
            okayValues.loc[idx,'Significance'] = data['Significance'][idx]

# Counting the number of items in the dataframe
print(goodValues)
goodSize = len(goodValues)
print("This is the number of values in the goodValues dataframe: " + str(goodSize))
print("\n")
print(okayValues)
okaySize = len(okayValues)
print("This is the number of observations in the okayValues dataframe: " + str(okaySize))
goodValues.to_pickle("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/goodValues.pkl")
okayValues.to_pickle("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/okayValues.pkl")

