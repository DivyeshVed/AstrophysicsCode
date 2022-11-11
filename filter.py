import pickle
import pandas as pd

# Looking at data from the Q and Sig Table
data = pickle.load(open("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/Q_Significance_Values.pkl","rb"))
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
# Creating a dataframe that will hold all the rcs values that represent qpos.
rcsValues = pd.DataFrame(columns = columnHeader)
# Creating a counter variable
counter = 0

# Filtering the data based on fundamental values only
for idx in data.index:
    FundQ = data['Fund.Q'][idx]
    FundSig = data['Fund.Sig'][idx]
    if ((FundSig == 'DNE') or (FundQ == 'DNE')):
        continue
    else: 
        FundSig = float(data['Fund.Sig'][idx])
        FundQ = float(data['Fund.Q'][idx])
        if ((FundSig >= 3.0) and (FundQ >= 2.0)):
            rcsValues.loc[idx,'OBSID'] = data['OBSID'][idx]
            rcsValues.loc[idx,'Best Fit Model'] = data['Best Fit Model'][idx]
            rcsValues.loc[idx,'Fund.Freq'] = data['Fund.Freq'][idx]
            rcsValues.loc[idx,'Fund.RCS'] = data['Fund.RCS'][idx]
            rcsValues.loc[idx,'Fund.RMS'] = data['Fund.RMS'][idx]
            rcsValues.loc[idx,'Fund.Q'] = data['Fund.Q'][idx]
            rcsValues.loc[idx,'Fund.Sig'] = data['Fund.Sig'][idx]
            rcsValues.loc[idx,'Harm.Freq'] = data['Harm.Freq'][idx]
            rcsValues.loc[idx,'Harm.RCS'] = data['Harm.RCS'][idx]
            rcsValues.loc[idx,'Harm.RMS'] = data['Harm.RMS'][idx]
            rcsValues.loc[idx,'Harm.Q'] = data['Harm.Q'][idx]
            rcsValues.loc[idx,'Harm.Sig'] = data['Harm.Sig'][idx]
            counter = counter + 1
            
print(rcsValues)
print("There are %s obsids that fall within the correct Sig value range"%str(counter))
rcsValues.to_pickle("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/sigQFilterValues.pkl")
rcsValues.to_excel("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/sigQFilterValues.xlsx")
data.to_pickle("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/Q_Significance_Values.pkl")