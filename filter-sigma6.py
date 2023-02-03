# This file contains code that filters out the data from the Q and Significance main table that has a significance greater than 6. 
# The reason this code is written is to confirm the presence of sigma > 6 in the observations on Dr. Arur's list. 
# Initially only the fundamental significance was being considered, but later on we also consider the harmoic significance.
import pickle
import pandas as pd

# Looking at data from the Q and Sig Table
data = pickle.load(open("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/Q_Significance_Values.pkl","rb"))
# Making column header list that will be used for the two tables formed in this code.
# columnHeader = ['OBSID', 'Significance']
columnHeader = ['OBSID', 'Significance', 'Fund', 'Har']
# Creating a dataframe that will hold all the rcs values that represent qpos.
Sig6Values = pd.DataFrame(columns = columnHeader)
# Creating a counter variable
counter = 0

# Filtering the data based on fundamental values only
for idx in data.index:
    FundSig = data['Fund.Sig'][idx]
    HarSig = data['Harm.Sig'][idx]
    if (FundSig == 'DNE'): 
        if (HarSig == 'DNE'):
            continue
        else :
            HarSig = float(data['Harm.Sig'][idx])
            if (HarSig >= 6.0):
                Sig6Values.loc[idx,'OBSID'] = data['OBSID'][idx]
                Sig6Values.loc[idx, 'Significance'] = data['Harm.Sig'][idx]
                Sig6Values.loc[idx, 'Fund'] = 'No'
                Sig6Values.loc[idx, 'Har'] = 'Yes'
                counter = counter + 1
            else:
                continue
    else: 
        FundSig = float(data['Fund.Sig'][idx])
        if (FundSig >= 6.0):
            Sig6Values.loc[idx,'OBSID'] = data['OBSID'][idx]
            Sig6Values.loc[idx, 'Significance'] = data['Fund.Sig'][idx]
            Sig6Values.loc[idx, 'Fund'] = 'Yes'
            Sig6Values.loc[idx, 'Har'] = 'No'
            counter = counter + 1
        else :
            if (HarSig == 'DNE'):
                continue
            else :
                HarSig = float(data['Harm.Sig'][idx])
                if (HarSig >= 6.0):
                    Sig6Values.loc[idx,'OBSID'] = data['OBSID'][idx]
                    Sig6Values.loc[idx, 'Significance'] = data['Harm.Sig'][idx]
                    Sig6Values.loc[idx, 'Fund'] = 'No'
                    Sig6Values.loc[idx, 'Har'] = 'Yes'
                    counter = counter + 1
                else:
                    continue
            
            
print(Sig6Values)
print("There are %s obsids that fall within the correct Sig value range"%str(counter))
Sig6Values.to_pickle("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/Sig6FHFilterValues.pkl")
Sig6Values.to_excel("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/Sig6FHFilterValues.xlsx")
data.to_pickle("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/Q_Significance_Values.pkl")