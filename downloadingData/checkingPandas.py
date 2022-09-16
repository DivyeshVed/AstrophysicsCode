# This file is used to check the pandas dataframe called newDataFrame. I think this was used in the trial and testing stages for pandasm when I was learning pandas. 

import pandas as pd
import pickle 

data = pickle.load(open("/Users/rohanpunamiya/Desktop/AstrophysicsCode/downloadingData/newDataFrame.pkl","rb"))
print(data)
