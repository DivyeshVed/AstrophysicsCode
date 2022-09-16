import pickle
import pandas as pd



data = pickle.load(open("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/Q_Significance_Values.pkl","rb"))
data1 = pickle.load(open("/Users/rohanpunamiya/Desktop/AstrophysicsCode/dataTable.pkl","rb"))
data = data.reset_index()
data = data.drop('index',axis = 1)
print(data)
columnHeader = ['OBSID','Frequency','Best Fit Model','RMS Value','Q Value','Significance']
goodValues = pd.DataFrame(columns = columnHeader)
okayValues = pd.DataFrame(columns = columnHeader)
# data.to_pickle("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/Q_Significance_Values.pkl")
for idx in data.index:
    # First correcting best fit model thing
    colonPosition = (data1["Best_Fit_Model"][idx]).find(":")
    print("This is the position of the colon in the string: " + str(colonPosition))
    numberStartIndex = colonPosition + 2
    print("This is the starting position of the numbers in the string: " + str(numberStartIndex))
    columnData = (data1["Best_Fit_Model"][idx])
    print("This is the column data we want to work with: " + str(columnData))
    numberData = columnData[numberStartIndex : len(columnData)]
    print("This is the value of numberData: " + str(numberData))
    print("\n")
    if numberData == "an":
        numberData = 0
    numberData = float(numberData)
    print("This is the number data that we are working with: " + str(numberData))
    if (numberData >= 0.7 and numberData <= 1.6):
        if (data['Frequency'][idx]) == 'DNE':
            data['Frequency'][idx] = 0
        elif float(data['Significance'][idx]) > 3.0:
            if (float(data['Q Value'][idx]) >= 2.0) and (float(data['Q Value'][idx] <= 30)):
                goodValues.loc[idx,'OBSID'] = data['OBSID'][idx]
                goodValues.loc[idx,'Q Value'] = data['Q Value'][idx]
                goodValues.loc[idx,'Significance'] = data['Significance'][idx]
                goodValues.loc[idx,'Frequency'] = data['Frequency'][idx]
                goodValues.loc[idx,'RMS Value'] = data['RMS Value'][idx]
                goodValues.loc[idx,'Best Fit Model'] = data1['Best_Fit_Model'][idx]
            elif (float(data['Q Value'][idx]) >= 1.0 and float(data['Q Value'][idx]) < 2.0):
                okayValues.loc[idx,'OBSID'] = data['OBSID'][idx]
                okayValues.loc[idx,'Q Value'] = data['Q Value'][idx]
                okayValues.loc[idx,'Significance'] = data['Significance'][idx]
                okayValues.loc[idx,'Frequency'] = data['Frequency'][idx]
                okayValues.loc[idx,'RMS Value'] = data['RMS Value'][idx]
                goodValues.loc[idx,'Best Fit Model'] = data1['Best_Fit_Model'][idx]

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

