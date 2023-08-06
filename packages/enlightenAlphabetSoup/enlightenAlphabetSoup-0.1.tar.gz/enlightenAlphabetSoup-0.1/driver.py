#Author: Yousuf Asfari
#Alphabet Soup Programming Challenge
import sys

def readFile(fileName):
    totalLines = []
    findList = []

    #Open the file for reading, line by line
    fp = open(fileName, 'r')
    line = fp.readline() 

    #Get the row and column count from line 1
    firstLine = line.split('x')
    rows = int(firstLine[0])
    cols = int(firstLine[1])

    #Collect all characters into a single list
    for currRow in range(rows):
        line = fp.readline() 
        currLine = line.split()
        totalLines = totalLines + currLine

    #After the matrix, collect words that we will be looking for
    for line in fp:
        line = line.rstrip()
        findList.append(line.replace(" ", ""))

    fp.close()
    return (cols, totalLines, findList)


def findmatch(letterList, word, pos, depth, initial, direction, cols):
    #Return Cases and Base Case
    #For return cases we use (-1, -1) to indicate a failed result, i.e. keep looking
    if (pos != -1):
        #If we surpass the target word's length
        if (depth + 1 > len(word)):
            return (-1, -1)

        #If the given index is not a valid one for the list
        if (pos < 0 or pos >= len(letterList)):
            return (-1, -1)

        #If the current position doesn't match the target word's
        if (letterList[pos] != word[depth]):
            return (-1, -1)

        #If we find a match and we are at the final character, return the initial and final positions
        if(letterList[pos] == word[depth] and depth + 1 == len(word)):
            return (initial, pos)
    
    #Recursive Case
    for charPos in range(len(letterList)):
        #Loop over all characters, but initially we want to start with all and recurse from every starting point possible
        if (initial == -1):
            #Possible crossword directions
            directionList = [-1, +1, -cols, +cols, -cols - 1, -cols + 1, +cols - 1, +cols + 1]
            for dir in directionList:
                #Start at every position with all possible directions
                first, last = findmatch(letterList, word, charPos, depth+1, charPos, dir, cols)
                if (first != -1):
                    return (first, last)
        else:
            #We don't want an invaid squiggly crossword solution, it has to follow the rules
            if ((charPos - pos) == direction):
                first, last = findmatch(letterList, word, charPos, depth+1, initial, direction, cols)
                if (first != -1):
                    return (first, last)
    return (-1, -1)


def output(item, firstRow, firstCol, lastRow, lastCol):
    print(item + " " + str(firstRow) + ":" + str(firstCol) + " " + str(lastRow) + ":" + str(lastCol))


if __name__ == "__main__":
    if(len(sys.argv) != 2):
        sys.exit("Must supply a file")

    cols, letterList, findList = readFile(sys.argv[1])

    #Loop through the words we need to find, and call findmatch on the list of all characters
    for item in findList:
        first, last = findmatch(letterList, item, -1, -1, -1, 0, cols)
        
        #Get the row and column value of the first and last characters using division and modulo
        firstRow = first // cols
        firstCol = first % cols

        lastRow = last // cols
        lastCol = last % cols    

        #Output to console the results for each item searched for
        output(item, firstRow, firstCol, lastRow, lastCol)
    


    