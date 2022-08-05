##This code if for viewing the dataframe and making adjustments to it (deleting rows, etc)

import pickle
import pandas as pd

fp = pd.read_pickle('/Users/erinhorbacz/Downloads/Research/testData/QPO_log.pkl')
#fp = fp.drop(4) ##deletes row 4
#fp.to_pickle('/Users/erinhorbacz/Downloads/Research/testData/QPO_log.pkl')

f = open("/Users/erinhorbacz/Downloads/Research/testData/QPO_log.pkl","rb")
data = pickle.load(f)
print(data.to_string()) ##prints dataframe to console


#bin_data = f.read()
#graph_data = pickle.loads(bin_data)
#print(graph_data)
#print(data['OBSID'])
#print(compile_info())
