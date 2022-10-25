import pickle
import pandas as pd

# Looking at data from the Q and Sig Table
data = pickle.load(open("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/testValues.pkl","rb"))
# Making column header list that will be used for the two tables formed in this code.
columnHeader = ['OBSID',
'Best Fit Model',
'Fund.Freq',
'Fund.RCS',
'Fund.RMS',
'Fund.Q',
'Fund.Sig',
'Harm.Freq',
'Harm.RCS',
'Harm.RMS',
'Harm.Q',
'Harm.Sig']
# Creating a dataframe that will hold all the good values that represent qpos.
goodValues = pd.DataFrame(columns = columnHeader)
# Creating a dataframe that will hold all the okay values that represent qpos.
okayValues = pd.DataFrame(columns = columnHeader)

# Filtering the data based on fundamental values only
for idx in data.index:
    FundRCS = data['Fund.RCS'][idx]
    if (FundRCS == 'DNE'):
        continue
    else: 
        FundRCS = float(data['Fund.RCS'][idx])
        # print("This is the fundamental RCS Values:",FundRCS,", that is the first parameter for filtering.")
        if (FundRCS >= 0.7 and FundRCS <= 1.6):
            if float(data['Fund.Sig'][idx]) > 3.0:
                if float(data['Fund.Q'][idx]) >= 2.0:
                    goodValues.loc[idx,'OBSID'] = data['OBSID'][idx]
                    goodValues.loc[idx,'Best Fit Model'] = data['Best Fit Model'][idx]
                    goodValues.loc[idx,'Fund.Freq'] = data['Fund.Freq'][idx]
                    goodValues.loc[idx,'Fund.RCS'] = data['Fund.RCS'][idx]
                    goodValues.loc[idx,'Fund.RMS'] = data['Fund.RMS'][idx]
                    goodValues.loc[idx,'Fund.Q'] = data['Fund.Q'][idx]
                    goodValues.loc[idx,'Fund.Sig'] = data['Fund.Sig'][idx]
                    goodValues.loc[idx,'Harm.Freq'] = data['Harm.Freq'][idx]
                    goodValues.loc[idx,'Harm.RCS'] = data['Harm.RCS'][idx]
                    goodValues.loc[idx,'Harm.RMS'] = data['Harm.RMS'][idx]
                    goodValues.loc[idx,'Harm.Q'] = data['Harm.Q'][idx]
                    goodValues.loc[idx,'Harm.Sig'] = data['Harm.Sig'][idx]
                elif (float(data['Fund.Q'][idx]) >= 1.0 and float(data['Fund.Q'][idx]) < 2.0):
                    okayValues.loc[idx,'OBSID'] = data['OBSID'][idx]
                    okayValues.loc[idx,'Best Fit Model'] = data['Best Fit Model'][idx]
                    okayValues.loc[idx,'Fund.Freq'] = data['Fund.Freq'][idx]
                    okayValues.loc[idx,'Fund.RCS'] = data['Fund.RCS'][idx]
                    okayValues.loc[idx,'Fund.RMS'] = data['Fund.RMS'][idx]
                    okayValues.loc[idx,'Fund.Q'] = data['Fund.Q'][idx]
                    okayValues.loc[idx,'Fund.Sig'] = data['Fund.Sig'][idx]
                    okayValues.loc[idx,'Harm.Freq'] = data['Harm.Freq'][idx]
                    okayValues.loc[idx,'Harm.RCS'] = data['Harm.RCS'][idx]
                    okayValues.loc[idx,'Harm.RMS'] = data['Harm.RMS'][idx]
                    okayValues.loc[idx,'Harm.Q'] = data['Harm.Q'][idx]
                    okayValues.loc[idx,'Harm.Sig'] = data['Harm.Sig'][idx]

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
goodValues.to_excel("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/goodValues.xlsx")
data.to_pickle("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/testValues.pkl")