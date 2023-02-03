# This file will contain the function that is used to extract the lines of code that we want to download.

def lineExtractor(file1, file2):
    counter = 0
    # Reading and iterating through every line in the file that contains all the codes
    for line in file2.readlines():
        # The first thing we do is look at the length of the line, as all the lines that have the correct download codes have a length of 185
        if len(line) == 186: 
            # We then look for the second last character. The second last character of a slue data code line is A or Z or G. 
            second_last_character = line[-3]
            if not (second_last_character == "A" or second_last_character == "Z" or second_last_character == "G"):
                file1.write(line)
                counter +=1 
    print(counter)

# We also need to extract the obsid from the line of code. The function below will help us do that and place the obsid in the pandas table
def obsidExtractor(file1):
    list1 = []
    list2 = []
    # Iterating through every line in the file that contains the lines of code that we are downloading
    for line in file1.readlines():
        forwardSlashPosition = line.rfind("//")
        currentObsid = line[forwardSlashPosition+9:forwardSlashPosition+23]
        list1.append(currentObsid)
        currentPrnb = line[forwardSlashPosition+2:forwardSlashPosition+8]
        list2.append(currentPrnb)
    return list1, list2