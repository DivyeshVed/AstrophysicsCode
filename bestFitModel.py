# This file takes into account all the rcs values for each fit model from the pandas table and finds the best fit model according to our creiterion. 
# This file checks for the qpo_fit folder inside the obsid folder, and for the best_model.txt inside the qpo_fit folder.
# It tells us the number of obsids that have the qpo_fit folder, and the ones that don't. 

import pickle
import pandas as pd
import sys
import os 
import numpy as np

# Loading the pkl file.
data1 = pickle.load(open("/Users/rohanpunamiya/Desktop/AstrophysicsCode/dataTable.pkl","rb"))
# Getting the column headers form the table. 
columnHeader = data1.columns
print(len(data1))
counter = 0
# Iterating through the data that is already present in the table. 
for a in data1.index:
    obsid = data1.loc[a,"OBSID"]
    print("This is the OBSID that we are looking at: " + str(obsid))
    # Getting the rcs values for the different models.
    value1 = float(data1.loc[a,"0.5 lor model"])
    value2 = float(data1.loc[a,"1 lor model"])
    value3 = float(data1.loc[a,"1.5 lor model"])
    value4 = float(data1.loc[a,"2 lor model"])
    value5 = float(data1.loc[a,"3 lor model"])
    value6 = float(data1.loc[a,"4 lor model"])
    # Putting all these values in a list.
    rcsList = [str(value1), str(value2), str(value3), str(value4), str(value5), str(value6)]
    print("This is the rcs list:")
    print(rcsList)
    # Creating an empty absValueList and nonZeroList
    absValueList = []
    nonZeroListIndex = []
    # Finding the values in the lisr that fall within a particular range.
    for b in range(len(rcsList)):
        item = rcsList[b]
        print("This is the item we are focusing on: " + item)
        if (float(item) <= 1.6 and float(item) >= 0.5):
            absValue = str(abs(float(item)-1.0))
            nonZeroListIndex.append(b)
            absValueList.append(absValue)
            print("Item was added to the absValueList and nonZeroListIndex")
        elif (float(item) > 1.6 or float(item) < 0.5) or (item == 'nan'):
            absValue = str(0)
            absValueList.append(absValue)
            print("Item was added to lists with a value of 0")
    # Printing the absValueList and the nonZeroIndexList
    print("This is the absValue list:")
    print(absValueList)
    print("This is the nonZeroIndexList:")
    print(nonZeroListIndex)
    # Getting all the values from the rcsList that are non zero and adding them to an interested list. 
    interestedList = []
    print("This is the length of the nonZeroListIndex: " + str(len(nonZeroListIndex)))
    if len(nonZeroListIndex) > 0:
        for c in range(len(nonZeroListIndex)):
            index = nonZeroListIndex[c]
            print("This is the index that we are working with from the nonZeroListIndex: " + str(index))
            interestedList.append(absValueList[index])   
        # Finding the minimum value in the interested list.
        print("This is the interested list:")
        print(interestedList)
        minimumValue = min(interestedList)
        print("This is the minimum value in the interested list: " + str(minimumValue))
        # Finding the index of the minimum value from the interested list.
        minValueIndex = absValueList.index(minimumValue)
        print("This is the minimum value index in the rcsList: " + str(minValueIndex))
        # You add 5 as there are 5 columns before the columns for the best model fits start. We want to find the index of the best fit model. 
        modelIndex = int(minValueIndex) + 5
        print("This is the modelIndex value: " + str(modelIndex))
        # Making the replace value that includes the modelIndex and the value at that index. 
        replaceValue = str(columnHeader[modelIndex] + ": " + rcsList[minValueIndex])
        # Printing out the replace value constructed above. 
        print("This is the replace value: " + str(replaceValue))
        data1.loc[a,"Best_Fit_Model"] = replaceValue
        counter = counter + 1
        print("The value has been replaced in the dataTable.pkl file")
    else:
        replaceValue = str('Nan')
        data1.loc[a,'Best_Fit_Model'] = replaceValue
    print("\n")
    print("This is the number of non-Nan values: " + str(counter))
# Saving the dataTable to a pickle file.
data1.to_pickle("/Users/rohanpunamiya/Desktop/AstrophysicsCode/dataTable.pkl") 