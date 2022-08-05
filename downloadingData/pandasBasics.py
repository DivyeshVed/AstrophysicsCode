import pandas as pd

#Loading data into a dataframe. This is used to read in a csv file.
#df = pd.read_csv('pokemon_data.csv')
#Loading the data into a dataframe from a txt file. Need to use the same function as reading a csv file, but need to specify a delimeter.
df = pd.read_csv('pokemon_data.txt',delimiter = '\t')

#Printing the pandas table
print(df)

#Printing the first 3 rows of the table
#print(df.head(3))

#Printing out the last 3 rows of the table
#print(df.tail(3))

#READING DATA IN PANDAS.
#Reading the headers
#print(df.columns)

#Reading each column from the table. This will print all the data in the column with the header Name.
#print(df['Name'])

#To print a specific range from a column. This will print the range 0 to 5 in the column with the header Name.
#print(df['Name'][0:5])

#If you want to get multiple columns. This will print out all the data in the columns with the header names Name and Type 1. You are basically stroing the names of the columsn that you want in a list.
#print(df[['Name','Type 1']])

#If you want to print out each row in the dataframe. Need to use the iloc function which stands for integer location. This will give you the data in teh first index in every column of the table.
#print(df.iloc[1])

#You can print out multiple rows. Simply use the colon to get the range.
#print(df.iloc[1:4])

#The same iloc function can be used to grab a particular location data in the table. It will give the [r,c] data that is specified.
#print(df.iloc[2,1])

#To iterate through each row in the table, you can use the following line of code. This will print out the data in each row seperately.
#for index, row in df.iterrows():
#    print(index,row)

#If you want to look for a particular string or data type in the table. The command will look for the Type 1 data that is equal to Fire, and only print the data that has this property.
#print(df.loc[df['Type 1'] == "Fire"])

##SORTING OR DESCRIBING THE DATA.
#This gives is the mean, the count, the standard deviation, the minimum value and the maximum value. This is given for each header.
#print(df.describe())

#If you want to sort the data by a particular column. This will sort the data based on the Name column, in an alphabetical order.
#print(df.sort_values("Name"))

#If you want to sort the data in descending order instead.
#print(df.sort_values("Name", ascending = False))

#If you want to sort data by several columns.
#print(df.sort_values(['Type 1','HP']))

#Sorting with several columns can be done either ascending or descending order. The sorts the data by Type 1 ascending and HP descending.
#print(df.sort_values(['Type 1','HP'], ascending = [1,0]))

##MAKING CHANGES TO THE DATA.
#Adding a new column to the data. This will add a new colum to the end of the table. We want the column to contain the total of all the numerical values.
#df['Total'] = df['HP'] + df['Attack'] + df['Defense'] + df['Sp. Atk'] + df['Sp. Def'] + df['Speed']
#print(df)

#If you want to drop a partciluar column. You need to reassign the dataframe.
#df = df.drop(columns = ['Total'])
#print(df)

#To add a column in a different way. This basically carries out the same function as the lines of code above while adding the total column. You are adding horizontally, so you set axis = 1, if vertically axis = 0.
#df['Total'] = df.iloc[:,4:10].sum(axis = 1)
#print(df)
