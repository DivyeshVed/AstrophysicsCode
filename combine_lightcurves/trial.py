import re
# Setting path to the datamode.txt file.
path = "/Users/divyeshved/Dropbox (Gatech)/CygX2/P40017/40017-02-01-00/datamode.txt"
intervalList = []
filePathList = []
# Opening the file and reading from it
with open(path, 'r') as file:
        for datamodeLineNumber, currentLine in enumerate(file):
            # Checking if there is SB in the file.
            if "SB" in currentLine:
                currentLineIndices = [m.start() for m in re.finditer("'", currentLine)]
                currentLineInfo = currentLine[currentLineIndices[0]+1: currentLineIndices[1]]
                intervalList += [currentLineInfo]
                nextLine = next(file, None)
                filePathList += [nextLine]
a = 0
b = 0
numberOfTimeIntervals = 1
while a < len(intervalList)-1:
    if intervalList[a] != intervalList[a+1]:
        numberOfTimeIntervals += 1
    a += 1
addingNumber = int((len(intervalList) / numberOfTimeIntervals))
print("Number of sub intervals in each time interval: " + str(addingNumber))
print("Number of time intervals: " + str(numberOfTimeIntervals))
print("Number of SB intervals: " + str(len(intervalList)))
subIntervalList1 = list(range(addingNumber))
subIntervalList2 = []
subIntervalList3 = []
finalList = []
if numberOfTimeIntervals == 2:
    for b in subIntervalList1:
        subIntervalList2 += [subIntervalList1[b] + addingNumber]
    for c in range(len(subIntervalList1)):
        finalList += [[subIntervalList1[c], subIntervalList2[c]]]
else:
    for d in subIntervalList1:
        subIntervalList2 += [subIntervalList1[d] + addingNumber]
    for e in subIntervalList1:
        subIntervalList3 += [subIntervalList1[e] + (2 * addingNumber)]
    for f in range(len(subIntervalList1)):
        finalList += [[subIntervalList1[f], subIntervalList2[f], subIntervalList3[f]]]
print("This is the final list of indexes that we should use to ge tthe file path from the filePathList: ")
print(finalList)
fileList = [filePathList for g in finalList]
print(fileList)

