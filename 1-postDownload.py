from 1.1-extractingLines import lineExtractor
from 1.1 extractingLines import obsidExtractor
import pandas as pd
import pickle

# This file will hold all the functions that need to be run on the download codes. 
# This file will be run on the txt file that contains all the downloaded codes, including the slue data.
# We will import all the functions from the other files into this file, and then run this one file only. 
def postDownload():
    # The first step would be to create the file that wil hold the new, downloadable data codes. 
    fileWrite = open("/Users/rohanpunamiya/Dropbox (GaTech)/Pipeline/codesToDownload.txt","w")

    # Reading through the file that is holding all the data code that are on the heasrsac website.
    # Make sure that the data codes are in the file, copied correctly from the hearsac website. 
    fileRead = open("/Users/rohanpunamiya/Dropbox (GaTech)/Pipeline/allCodes.txt","r")

    # Calling the function that will get us out desired data code lines and print them into the file created in the first step. 
    lineExtractor(fileWrite, fileRead)
    fileWrite.close()

    # Opening the file that contains only the data codes that we want to download, in order to read the obsid from this file
    fileRead2 = open("/Users/rohanpunamiya/Dropbox (GaTech)/Pipeline/codesToDownload.txt","r")

    # Calling the file that will extract the prnbs and obsids from the download codes and store them in appropriate lists
    obsidList, prnbList = obsidExtractor(fileRead2)

    # Creating a dataframe with the desired column headers.
    df = pickle.load(open("/Users/rohanpunamiya/Dropbox (GaTech)/Pipeline/firstDataFrame.pkl","rb"))

    # Iterating through the obsidList and putting it into the column in the dataframe
    i = 1
    while i < len(obsidList):
        df.at[i,'OBSID'] = obsidList[i]
        df.at[i,'prnb'] = prnbList[i]
        df.at[i,'Target Name'] = "Cygnus X-2"
        df.at[i,'Status'] = "Archived"
        i += 1
    print(df)

    # Saving a dataframe in a file. 
    df.to_pickle("/Users/rohanpunamiya/Dropbox (GaTech)/Pipeline/firstDataFrame.pkl")
