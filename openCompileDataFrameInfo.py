# This file is used to make the Compile dataframeInfo.pkl file and then opens the file inthe various ways. 

import pandas as pd
import pickle
import sys

# columnHeader = ['NAME',
#  'OBSID',
#  'INDIVIDUAL OBS',
#  'OBSDATE',
#  'TIME',
#  'GTI',
#  'COUNTRATE',
#  'HARDNESS_RATIO']
 
# compileDataFrameInfo = pd.DataFrame(columns = columnHeader)
# compileDataFrameInfo.to_pickle("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/compile_dataframe_info.pkl")

input = sys.argv[1]
data = pickle.load(open("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/compile_dataframe_info.pkl", "rb"))
if (input == "print"):
    print(data.to_string())
elif (input == "clear"):
    data.drop(data.index,inplace=True)
data.to_pickle("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/compile_dataframe_info.pkl")
