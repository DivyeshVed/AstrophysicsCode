# Import the pandas and pickle libraries
import pandas as pd
import pickle
import os
from os.path import exists

# Loading the pkl file.
data = pickle.load(open("/Users/rohanpunamiya/Desktop/AstrophysicsCode/dataTable.pkl","rb"))
print(data.to_string())

