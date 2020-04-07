# NAME: Charles Rawlins, Kyle Whitlatch
# DATE: 4/10/2020
# FILE: Homework 3

from tkinter import *
from itertools import compress
from math import gcd

# Global class to handle global vars for both problems
class GlobVars:
    pass


# Adds a string to the broadcast schedule (likely always a chunk)
def addbroad(newString):
    GlobVars.broadcastString = GlobVars.broadcastString + " |" +newString + "| "


# Increments the unique counter to handle which chunk gets broadcast
def incChunkCounter(diskIdx):
    GlobVars.cntrList[diskIdx] += 1
    if GlobVars.cntrList[diskIdx] >= GlobVars.sizes[diskIdx]:
        GlobVars.cntrList[diskIdx] = 0


# Broadcast a chunk with a given index
def broadcastChunk(j,k):
    addbroad(GlobVars.chunks[j][k])
    incChunkCounter(j)


# Initializes the counters for each of the chunks
def initCntrs():
    cntrList = []
    for i in range(len(GlobVars.sizes)):
        cntrList.append(0)

    GlobVars.cntrList = cntrList


# Displays the broadcast schedule when finished.
def displayBroadcast():
    print(GlobVars.broadcastString)


# Main function that creates the broadcast schedule
def createSchedule(dataEntry, probEntry):
    print("Processing Input Data...")
    dataProbs = probEntry.get()
    dataPages = dataEntry.get()
    dataProbs = list(dataProbs)
    dataPages = list(dataPages)

    assert len(dataProbs) == len(dataPages)

    uniqueProbs = list(set(dataProbs))
    uniqueProbs.sort()
    numDisks = len(uniqueProbs)

    diskArray = []
    tempBool = []
    boolArray = []

    # Sort data into disks
    for freq in uniqueProbs:

        tempBool = []

        for prob in dataProbs:

            if prob == freq:
                tempBool.append(True)
            else:
                tempBool.append(False)

        diskArray.append(list(compress(dataPages,tempBool)))

    print("Sorted data into disks!")

    # Get disk sizes
    sizeList = []
    for diskList in diskArray:
        sizeList.append(len(diskList))

    maxDiskSize = max(sizeList)
    numDisks = len(sizeList)

    # Find LCM
    lcm = sizeList[0]
    for i in sizeList[1:]:
        lcm = lcm * i // gcd(lcm, i)

    print("Disk Size LCM = : " + str(lcm))

    # Get Relative Frequencies
    relFreqList = []
    for i in sizeList:
        relFreqList.append(int(lcm / i))

    print("Generated Relative Freqs: " + str(relFreqList))

    # Get lcm of relative frequencies
    lcm = relFreqList[0]
    for i in relFreqList[1:]:
        lcm = lcm * i // gcd(lcm, i)

    print("RelFreq LCM = : " + str(lcm))
    maxChunks = lcm

    # Calc Number of chunks
    numChunkList = []
    for relFreq in relFreqList:
        numChunkList.append(int(maxChunks/relFreq))

    # Check if disk sizes are multiples of each other, if so, then chunk size can increase for larger disks
    isMultiple = True
    for size in sizeList:
        if (maxDiskSize % size) != 0:
            isMultiple = False
            break


    GlobVars.isMultiple = isMultiple
    if GlobVars.isMultiple:
        newChunkSize = sizeList[-2]
        for i in range(len(sizeList)-1,len(sizeList)):
            numChunkList[i] = int(numChunkList[i]/newChunkSize)

        chunklcm = numChunkList[0]
        for i in numChunkList[1:]:
            chuncklcm = chunklcm * i // gcd(chunklcm, i)

        if (chuncklcm != lcm):
            maxChunks = chuncklcm

        # Reset max chunks to reduce looping
        # maxChunks = max(numChunkList)

    # Create Chunks
    chunkList = []
    if isMultiple != True:
        for numChunks,size,disk in zip(numChunkList, sizeList,diskArray):
            chunksize = int(size/numChunks) # Should always be one
            # assert chunksize == 1
            tempList = []
            if chunksize == 1:
                tempList = list([x for x in disk])
            else:
                for i in range(0, len(disk), chunksize):
                    tempString = ""
                    for j in range(i, i + chunksize):
                        tempString = tempString + disk[j]
                    tempList.append(tempString)
            chunkList.append(tempList)
    else:
        print("MULTIPLE CASE!")
        for numChunks,size,disk in zip(numChunkList, sizeList,diskArray):
            chunksize = int(size/numChunks) # May not be one
            tempList = []

            for i in range(0,len(disk),chunksize):
                tempString = ""
                for j in range(i,i+chunksize):
                    tempString = tempString + disk[j]
                tempList.append(tempString)

            chunkList.append(tempList)

    # Run main broadcast loop and printout broadcast
    GlobVars.broadcastString = "BROADCAST:"
    GlobVars.chunks = chunkList
    GlobVars.sizes = sizeList
    initCntrs() # Init loop counters for each disk rather than indexing by j and k
    for i in range(maxChunks):
        addbroad("!")
        for j in range(numDisks):
            k = i % numChunkList[j]
            broadcastChunk(j,k)

    displayBroadcast()
    print("Done!")


# Handles window geometry for problem 1
def problem1Func( mainWindow):
    probX = 200
    probY = 150
    probWindow = Toplevel(mainWindow)
    probWindow.geometry(str(probX) + "x" + str(probY))
    probWindow.title("Brodcast Scheduling with Multidisk")

    # Setup User input GUI
    commandX = 0
    commandY = 0
    probWidgetWidth = 180
    widgetYSpace = 20
    enterLabel = Label(probWindow, text="Enter a Schedule Program:",font="Helvetica 10 bold")
    enterLabel.place(x=commandX,y=commandY, width=probWidgetWidth)
    dataLabel = Label(probWindow, text="Enter broadcast data pages:", font="Helvetica 10")
    dataLabel.place(x=commandX, y=commandY + widgetYSpace, width=probWidgetWidth)
    dataEntry = Entry(probWindow)
    dataEntry.place(x=commandX, y=commandY + 2*widgetYSpace, width=probWidgetWidth)
    probLabel = Label(probWindow, text="Enter broadcast page probs:", font="Helvetica 10")
    probLabel.place(x=commandX, y=commandY + 3*widgetYSpace, width=probWidgetWidth)
    probEntry = Entry(probWindow)
    probEntry.place(x=commandX, y=commandY + 4 * widgetYSpace, width=probWidgetWidth)
    genButton = Button(probWindow, text="Generate Schedule!", command=lambda: createSchedule(dataEntry, probEntry))
    genButton.place(x=commandX, y=commandY + 5*widgetYSpace, width=probWidgetWidth)


###################PROBLEM 2 FUNCS##############################


# Increment the broadcast index (acts like 'time')
def incrBroadcastIdx():
    GlobVars.broadcastIdx += 1
    GlobVars.movingTime += 1
    if GlobVars.broadcastIdx >= GlobVars.broadcastLength:
        GlobVars.broadcastIdx = 0 # restart broadcast loop


# Computes the p values for each of the recieved data items
def computePVals(newItem):
    tempItemList = []

    haveEntry = False

    for diskCache in GlobVars.cacheArray:
        for entry in diskCache:
            if newItem == entry:
                haveEntry = True

    # Check if newitem is already in caches
    if haveEntry == False:
        tempItemList.append(newItem)

    if (GlobVars.cacheEmpty != True):
        for diskCache in GlobVars.cacheArray:
            for entry in diskCache:
                if entry != "":
                    tempItemList.append(entry)

    pInit = 0
    for pitem in tempItemList:
        pitemidx = GlobVars.uniqueData.index(pitem)
        # Compute P value
        if pitem == newItem:
            GlobVars.PVals[pitemidx] = (GlobVars.cval/((GlobVars.movingTime + 1) - GlobVars.tinitArray[pitemidx])) + (1 - GlobVars.cval) * GlobVars.PVals[pitemidx]
            GlobVars.tinitArray[pitemidx] = GlobVars.movingTime + 1 # Update time item was last accessed

    print("#####P-VAL CALCS#####")
    for i in range(len(GlobVars.PVals)):
        print("P-VAL: p(" + GlobVars.uniqueData[i] + ") = " + str(GlobVars.PVals[i]))


# Updates the cache with new entry if applicable
def updateCache(newItem):
    GlobVars.cacheEmpty = False

    # Check if newItem is already in cache, then don't do anything
    for diskCache in GlobVars.cacheArray:
        for entry in diskCache:
            if newItem == entry:
                print("NO NEED TO UPDATE CACHE!")
                return

    # Item not in cache, potentially add it to cache
    GlobVars.totalCacheNum += 1

    # Check which item needs to boot, then do so
    bootItem = ""
    if GlobVars.totalCacheNum > GlobVars.cachePerDisk:
        GlobVars.totalCacheNum -= 1
        # Compute lix values for cache only and pick item to boot
        bootItem = computeLIX()
        if bootItem == newItem:
            return # Dont update cache with new values
        else: # Remove boot item and replace with new item in for loop below
            for cache in GlobVars.cacheArray:
                for entry in cache:
                    if entry == bootItem:
                        entry = ""

    # Update caches with new item
    for disk in GlobVars.diskArray:
        if newItem in disk:
            diskIdx = GlobVars.diskArray.index(disk)
            for i in range(len(GlobVars.cacheArray[diskIdx])):
                if GlobVars.cacheArray[diskIdx][i] == "":
                    GlobVars.cacheArray[diskIdx][i] = newItem
                    return # found empty spot, return

    printString = ""
    for cache in GlobVars.cacheArray:
        for entry in cache:
            if entry != "":
                printString = printString + entry + ","

    print("CACHE CONTENTS: " + printString)


# Computes the Lix values for data entries in the cache
def computeLIX():
    tempLixList = []

    # Get all entries in current cache
    for cache in GlobVars.cacheArray:
        for entry in cache:
            if entry != "":
                tempLixList.append(entry)

    # Get frequencies for each cache item
    diskFreqVals = []
    for disk in GlobVars.diskArray:
        for entry in tempLixList:
            if entry in disk:
                diskidx = GlobVars.diskArray.index(disk)
                diskFreqVals.append(GlobVars.diskFreqs[diskidx])

    lixVals = []
    for i in range(len(tempLixList)):
        dataItem = tempLixList[i]
        dataPVal = GlobVars.PVals[GlobVars.uniqueData.index(dataItem)]
        lixVals.append(dataPVal/diskFreqVals[i])

    # Boot item with smallest lix value
    minLix = min(lixVals)
    bootIdx = lixVals.index(minLix)
    bootItem = tempLixList[bootIdx]
    bootItem = GlobVars.uniqueData[GlobVars.uniqueData.index(bootItem)]
    print("BOOTING ITEM:" + str(bootItem))
    return bootItem


# Satisifies individual needs for the client
def satisfyClientNeeds(newItem):
    satisfyList = []
    satisfyList.append(newItem)

    if(GlobVars.cacheEmpty != True):
        for diskCache in GlobVars.cacheArray:
            for entry in diskCache:
                if entry != "":
                    satisfyList.append(entry)

    while(True):
        canSatisfy = False
        for i in range(len(satisfyList)): # Loop through each current item and satisfy all availible needs
            if GlobVars.clientNeedsList[GlobVars.satisfyIdx] == satisfyList[i]:
                print("SATISFIED CLIENT NEED WITH: " + satisfyList[i])
                canSatisfy = True
                GlobVars.clientNeeds[GlobVars.satisfyIdx] = True
                GlobVars.satisfyIdx += 1
                if GlobVars.satisfyIdx >= len(GlobVars.clientNeedsList):
                    return

        if canSatisfy == False:
            return # Been through all current items and satisfied all client needs


# Checks if all needs of the client are met
def checkClientSatisfied():
    for check in GlobVars.clientNeeds:
        # Check each need individually, return false if any needs not met
        if check == False:
            return False

    # All needs met!
    return True


# Main function that governs creating the lix schedule
def lixSchedule(broadEntry, needEntry,cacheEntry):
    cval = 0.5
    GlobVars.cval = cval
    broadcastList = list(broadEntry.get())
    broadcastLength = len(broadcastList)
    uniqueData = list(set(broadcastList))
    uniqueData.sort()
    clientNeedsList = list(needEntry.get())
    clientNeeds = [False] * len(clientNeedsList)
    cachePerDisk = int(cacheEntry.get())
    totalCacheNum = 0
    GlobVars.totalCacheNum = totalCacheNum
    GlobVars.cachePerDisk = cachePerDisk

    # Preprocess data to get frequencies
    freqItemList = []
    for uniqueItem in uniqueData:
        tempCntr = 0
        for item in broadcastList:
            if item == uniqueItem:
                tempCntr += 1

        freqItemList.append(tempCntr)

    diskFreqs = list(set(freqItemList))
    numDisks = len(diskFreqs)
    diskArray = []

    for diskFreq in diskFreqs:
        tempList = []
        for freq,item in zip(freqItemList, uniqueData):
            if diskFreq == freq:
                tempList.append(item)

        diskArray.append(tempList)

    GlobVars.diskFreqs = diskFreqs
    GlobVars.diskArray = diskArray
    GlobVars.clientNeeds = clientNeeds
    GlobVars.clientNeedsList = clientNeedsList
    print("Sorted data into disks!")
    print("###################BEGIN STEPS##################")

    # Generate cache array
    cacheArray = []
    for j in range(numDisks):
        tempList  = []
        for i in range(cachePerDisk):
            tempList.append("")

        cacheArray.append(tempList)

    GlobVars.cacheArray = cacheArray

    # Start main recieved loop and setup global vars
    GlobVars.broadcastIdx = -1 # to start at 0
    GlobVars.satisfyIdx = 0
    GlobVars.cacheEmpty = True
    GlobVars.broadcastLength = broadcastLength
    GlobVars.uniqueData = uniqueData
    GlobVars.PVals = []
    GlobVars.tinitArray = []
    GlobVars.movingTime = -1
    for i in range(len(uniqueData)):
        GlobVars.tinitArray.append(0)
    for i in range(len(uniqueData)):
        GlobVars.PVals.append(0)

    while (True):
        # Increment broadcast list counter
        incrBroadcastIdx()
        # Get new data item
        newItem = broadcastList[GlobVars.broadcastIdx]
        # Print step
        print("______________________")
        print("STEP #" + str(GlobVars.movingTime + 1))
        print("RECIEVED ITEM:" + newItem)
        # Compute p for all current items
        computePVals(newItem)

        # Check to see if new data is added to cache and if any data is booted
        # Compute Lix if too much data is recieved, make sure keep to cacheperdisk limits
        updateCache(newItem)

        # Check if incoming data satisifies client needs and if any data in cache does as well
        satisfyClientNeeds(newItem)

        # Break if recieved all items client needs
        if checkClientSatisfied():
            break

    print("CLIENT RECIEVED ALL DATA!")


# Handles window geometry for problem 2
def problem2Func(mainWindow):
    probX = 250
    probY = 200
    probWindow = Toplevel(mainWindow)
    probWindow.geometry(str(probX) + "x" + str(probY))
    probWindow.title("LIX Caching Scheme")

    # Setup User input GUI
    commandX = 0
    commandY = 0
    probWidgetWidth = 250
    widgetYSpace = 20
    enterLabel = Label(probWindow, text="Enter a LIX Broadcast and Needs:", font="Helvetica 10 bold")
    enterLabel.place(x=commandX, y=commandY, width=probWidgetWidth)
    broadLabel = Label(probWindow, text="Enter broadcast data:", font="Helvetica 10")
    broadLabel.place(x=commandX, y=commandY + widgetYSpace, width=probWidgetWidth)
    broadEntry = Entry(probWindow)
    broadEntry.place(x=commandX, y=commandY + 2 * widgetYSpace, width=probWidgetWidth)
    needLabel = Label(probWindow, text="Enter client needs:", font="Helvetica 10")
    needLabel.place(x=commandX, y=commandY + 3 * widgetYSpace, width=probWidgetWidth)
    needEntry = Entry(probWindow)
    needEntry.place(x=commandX, y=commandY + 4 * widgetYSpace, width=probWidgetWidth)
    cacheLabel = Label(probWindow, text="Cache/Disk:", font="Helvetica 10")
    cacheLabel.place(x=commandX, y=commandY + 5*widgetYSpace, width=probWidgetWidth)
    cacheEntry = Entry(probWindow)
    cacheEntry.place(x=commandX, y=commandY + 6*widgetYSpace, width=probWidgetWidth)
    genButton = Button(probWindow, text="Generate LIX Prog!", command=lambda: lixSchedule(broadEntry, needEntry,cacheEntry))
    genButton.place(x=commandX, y=commandY + 7 * widgetYSpace, width=probWidgetWidth)

# Main function, has setup for problem selection window.
if __name__ == "__main__":

    mainWindow = Tk()
    mainWindow.title("Homework 3")
    globalX = 200
    globalY = 150
    mainWindow.geometry([str(globalX) + "x" + str(globalY)])
    startY = 5
    widgetYSpace = 20
    widgetWidth = 150
    widgetX = globalX/2 - widgetWidth/2

    selectLabel = Label(mainWindow, text="Select a Problem:")
    selectLabel.place(x=widgetX, y=startY, width=widgetWidth)
    problem1But = Button(mainWindow, text="Broadcast Scheduling",command=lambda: problem1Func(mainWindow))
    problem1But.place(x=widgetX, y=startY + widgetYSpace, width=widgetWidth)
    problem2But = Button(mainWindow, text="LIX Caching Scheme",command= lambda: problem2Func(mainWindow))
    problem2But.place(x=widgetX, y=startY + 3*widgetYSpace, width=widgetWidth)

    mainWindow.mainloop()


