import pandas as pd
import pickle

# This file takes in the fundamental frequency from the big table and adds it to a smaller table that is used to access these values for running qpo_fit_code_old.py
column_names = ['PRNB', 'OBSID', 'Frequency']
df = pd.DataFrame(columns = column_names)
data = pickle.load(open("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/Q_Significance_Values.pkl","rb"))
for idx in data.index:
    obsid = data["OBSID"][idx]
    prnb = "P" + obsid[0:5]
    df.loc[idx,'PRNB'] = prnb
    df.loc[idx,'OBSID'] = obsid
    df.loc[idx,'Frequency'] = data['Fund.Freq'][idx]

print(df.to_string())
df.to_pickle("/Users/rohanpunamiya/Dropbox (GaTech)/NS_Data/CygX2/frequencyTable.pkl")
