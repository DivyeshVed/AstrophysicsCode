import pickle

data = pickle.load(open("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/goodValues.pkl","rb"))
print(data.to_string())

data1 = pickle.load(open("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/okayValues.pkl","rb"))
print(data1.to_string())
