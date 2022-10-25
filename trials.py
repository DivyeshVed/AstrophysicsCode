# import pickle

# data1 = pickle.load(open("/Users/rohanpunamiya/Desktop/AstrophysicsCode/dataTable.pkl","rb"))
# print(data1.to_string())

import pandas as pd
import pickle
import os

# Opening the dataTable.pkl table. 
# data = pickle.load(open("/Users/rohanpunamiya/Desktop/AstrophysicsCode/dataTable.pkl","rb"))
# print(data.to_string())
# del data['Best_Fit_Model']

# # Opening the QandSignificanceValues.pkl table
# data = pickle.load(open("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/Q_Significance_Values.pkl","rb"))
# data = data.reset_index()
# print(data.to_string())
# data.to_pickle("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/Q_Significance_Values.pkl")

# data = pickle.load(open("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/goodValues.pkl","rbp"))
# print(data.to_string())

""" import pickle
import pandas as pd
import sys
import os 
import numpy as np

# Loading the pkl file.
data1 = pickle.load(open("/Users/rohanpunamiya/Desktop/AstrophysicsCode/dataTable.pkl","rb"))
# Getting the column headers form the table. 
columnHeader = data1.columns
print(len(data1))
data1['Best_Fit_Model'] = 0

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
        if (float(item) <= 1.6 and float(item) >= 0.7):
            absValue = str(abs(float(item)-1.0))
            nonZeroListIndex.append(b)
            absValueList.append(absValue)
            print("Item was added to the absValueList and nonZeroListIndex")
        elif (float(item) > 1.6 or float(item) < 0.7) or (item == 'nan'):
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
        print("The value has been replaced in the dataTable.pkl file")
    else:
        replaceValue = str('Nan')
        data1.loc[a,'Best_Fit_Model'] = replaceValue
    print("\n")
    
# # Saving the dataTable to a pickle file.
# data1.to_pickle("/Users/rohanpunamiya/Desktop/AstrophysicsCode/dataTable.pkl") """
# data = pickle.load(open("/Users/rohanpunamiya/Desktop/AstrophysicsCode/dataTable.pkl","rb"))
# for idx in data.index:
#     colonPosition = (data["Best_Fit_Model"][idx]).find(":")
#     print("This is the position of the colon in the string: " + str(colonPosition))
#     numberStartIndex = colonPosition + 2
#     print("This is the starting position of the numbers in the string: " + str(numberStartIndex))
#     columnData = (data["Best_Fit_Model"][idx])
#     print("This is the column data we want to work with: " + str(columnData))
#     numberData = float(columnData[numberStartIndex : len(columnData)])
#     print("This is the number data that we are working with: " + str(numberData))
#     rcsValueInRange = True
#     if (numberData >= 0.7 and numberData <= 1.6):
#         print("Contains rcs value wihtin range: " + str(rcsValueInRange))
#     else :
#         rcsValueInRange = False
#         print("This obsid does not contain a qpo in the right rcs range: " + str(rcsValueInRange))
#     print("\n")

# data = pickle.load(open("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/goodValues.pkl","rb"))
# data = pickle.load(open("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/Q_Significance_Values.pkl","rb"))
# print(data.to_string())
# print("This is the number of observations that we have found to have good values: " + str(len(data)))

data = pickle.load(open("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/Q_Significance_Values.pkl","rb"))
# # data = data.reset_index()
# data = data.drop('level_0',axis = 1)
print(data.to_string())
data.to_pickle("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/Q_Significance_Values.pkl")

""" prnbPath = '/Users/rohanpunamiya/Dropbox (GaTech)/CygX2'
obsidList = os.listdir(prnbPath)
for a in range(len(obsidList)):
    print(obsidList[a]) """
