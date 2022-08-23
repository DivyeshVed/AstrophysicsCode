import os
os.chdir("/Users/rohanpunamiya/Desktop/Data/P10066/10066-01-01-00/qpo_fit")
with open ("512lc_1024_3lor_log.log") as file:
    lineNumber = 0
    for line in file.readlines():
        print(lineNumber)
        if lineNumber == 117:
            print(line)
        lineNumber = lineNumber + 1