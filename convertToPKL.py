# This file can be used to convert a excel file to a PKL file. This converstion then allows us for easy comparison with our other PKL file.

import pickle
import pandas as pd

# The two lines below convert the excel file to the PKL file.
# df=pd.read_excel("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/6sigma_QPO_list.xlsx") # Path of the file. 
# df.to_pickle("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/6sigma_QPO_list.pkl")

# Printing the 6sigma_QPO_list.pkl and resetting the indexing as it got messed up.
data = pickle.load(open("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/6sigma_QPO_list.pkl","rb"))
data = data.drop('level_0',axis = 1)
data.to_pickle("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/6sigma_QPO_list.pkl")
print(data.to_string())
