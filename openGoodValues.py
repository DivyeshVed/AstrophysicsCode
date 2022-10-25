import pickle

data = data = pickle.load(open("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/goodValues.pkl","rb"))
print(data.to_string())
data.to_pickle("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/goodValues.pkl")