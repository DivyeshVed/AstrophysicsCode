# This file takes into account all the rcs values for each fit model from the pandas table and finds the best fit model according to our creiterion. 

import pickle
import pandas as pd

# Loading the pkl file.
data = pd.read_pickle(open("/Users/rohanpunamiya/Desktop/AstrophysicsCode/dataTable.pkl","rb"))
columnHeader = data.columns

for i in range(len(data)):
    # Getting the rcs values for the different models.
    value1 = float(data.loc[i,"0.5 lor model"])
    value2 = float(data.loc[i,"1 lor model"])
    value3 = float(data.loc[i,"1.5 lor model"])
    value4 = float(data.loc[i,"2 lor model"])
    value5 = float(data.loc[i,"3 lor model"])
    value6 = float(data.loc[i,"4 lor model"])
    rcsList = [value1, value2, value3, value4, value5, value6]
    # Subtracting 1 from these rcs values and taking the absolute value
    absValue1 = abs(value1 - 1)
    absValue2 = abs(value2 - 1)
    absValue3 = abs(value3 - 1)
    absValue4 = abs(value4 - 1)
    absValue5 = abs(value5 - 1)
    absValue6 = abs(value6 - 1)
    # Putting all these abs vaules into a list and finding the minimum value and it's index
    absValueList = [absValue1, absValue2, absValue3, absValue4, absValue5, absValue6]
    print(absValueList)
    minValue = min(absValueList)
    print(minValue)
    minValueIndex = absValueList.index(minValue)
    print(minValueIndex)
    modelIndex = minValueIndex + 5
    replaceValue = columnHeader[modelIndex] + ": " + str(rcsList[minValueIndex])
    print(replaceValue)
    data.loc[i, "Best Fit Model (RCS)"] = replaceValue
    
data.to_pickle("/Users/rohanpunamiya/Desktop/AstrophysicsCode/dataTable.pkl")


    

    
    