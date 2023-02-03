import pickle
import sys

input = sys.argv[1]
data = pickle.load(open("/Users/rohanpunamiya/Dropbox (GaTech)/NS_Data/CygX2/QandSigValuesTable.pkl","rb"))
if input == "clear": 
    data.drop(data.index,inplace=True)
elif input == 'sort':
    data = data.sort_values(by='OBSID')
elif input == 'reset_index':
    data = data.reset_index()
    data = data.drop('index',axis = 1)
elif input == 'print':
    print(data.to_string())
data.to_pickle("/Users/rohanpunamiya/Dropbox (GaTech)/NS_Data/CygX2/QandSigValuesTable.pkl")