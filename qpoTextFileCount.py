import os
import pandas as pd
 
path = '/Users/rohanpunamiya/Dropbox (GaTech)/CygX2'
totalObsidList = os.listdir(path)
check = 'P'
prnbList = [idx for idx in totalObsidList if idx[0].lower() == check.lower()]
qpoFolderExists = 0
qpo0exists = 0
qpo1exists = 0
qpoFileDNE = 0
qpoFolderDNE = 0
qpo1and0List = []
qpo0List = []
qpoFileDNEList = []
qpoFolderDNEList = []
for a in range(len(prnbList)):
    prnb = prnbList[a]
    newPath = path + '/' + prnb
    os.chdir(newPath)
    obsidList = os.listdir(newPath)
    for b in range(len(obsidList)s):
        obsid = obsidList[b]
        qpoFolderPath = newPath + '/' + obsid + '/' + 'qpo_fit'
        if (os.path.isdir(qpoFolderPath)):
            qpoFolderExists = qpoFolderExists + 1
            fileName1path = qpoFolderPath + '/' + 'qpo_0.txt'
            fileName2path = qpoFolderPath + '/' + 'qpo_1.txt'
            if os.path.exists(fileName1path):
                if os.path.exists(fileName2path):
                    qpo0exists = qpo0exists + 1
                    qpo1exists = qpo1exists + 1
                    qpo1and0List.insert(0,obsid)
                
                else:
                    qpo0exists = qpo0exists + 1
                    qpo0List.insert(0,obsid)
            else:
                qpoFileDNEList.insert(0,obsid)
                qpoFileDNE = qpoFileDNE + 1
        else:
            qpoFolderDNE = qpoFolderDNE + 1
            qpoFolderDNEList.insert(0,obsid)
print("This is a list of all obsids that contain both qpo0 and qpo1 txt files:")
for c in range(len(qpo1and0List)):
    print(qpo1and0List[c])
print("There are %s obsids that have both qpo_0.txt and qpo1_txt files" % str(qpo0exists + qpo1exists))
print("This is a list of all the obsids that only contain qpo0 txt file:")
for d in range(len(qpo0List)):
    print(qpo0List[d])
print("There are %s obsids that have only qpo_0.txt files" % str(qpo0exists))
            
# Adding the list to an excel file.
df = pd.DataFrame(qpo1and0List)
df1 = pd.DataFrame(qpo0List)
df.to_excel("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/qpo0and1FilesPresent.xlsx")
df1.to_excel("/Users/rohanpunamiya/Dropbox (GaTech)/CygX2/qpo0FilesPresent.xlsx")
