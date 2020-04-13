#Encode a byte string with parity bits 
import math
import numpy as np

def determineNumBits(stringLength):
    lowerK = int(math.ceil(math.log(stringLength,2)))
    #print(lowerK)

    while 2**lowerK < stringLength + lowerK + 1:
        #print("doing it ")
        lowerK += 1
    
    return lowerK

def encoder(bitString):
    #print(len(bitString))

    numParityBits = determineNumBits(len(bitString))
    bitStringList = list(bitString)
    for i in range(numParityBits):
        bitStringList.insert((2**i)-1,'p'+str(i+1))

    #print(bitStringList)

    def evaluateParity(p_index, space):

        #print("space " + str(space))
        #print("pindex " + str(p_index))
        counter = p_index
        parity = True
        skip = False
        while counter < totalLength:
            if skip: 
                counter += space
            else:
                for i in range(space):
                    if bitStringList[counter] == "1":
                        #print("1 occurs at" + str(counter))
                        parity = not parity
                    counter += 1
                    if counter >= totalLength:
                        return parity
            skip = not skip
        return parity

    
    for i in range(numParityBits):
        indexOfParity = (2**i)-1
        spacing = 2**i
        totalLength = len(bitStringList)
        bitStringList[indexOfParity] = "0" if evaluateParity(indexOfParity,spacing) else "1"
    toPrintFinal = "".join(bitStringList)
    parityBitsList = []

    for i in range(numParityBits):
        indexOfParity = (2**i)-1
        parityBitsList.append(bitStringList[indexOfParity])

    returnBitString = toPrintFinal
    #print("this is the count of 1's" + str(bitStringList.count("1")))
    returnOverallParityBit = "1" if (bitStringList.count("1")%2==1) else "0"

    #print("encoded hamming string " + returnBitString)
    #print("overall parity bit " + returnOverallParityBit)
    #print("list of parity bits without overall " + str(parityBitsList))

    return [returnBitString,returnOverallParityBit, parityBitsList]


def decoder(encodedString, overallParity):
    numParityBits =  int(math.ceil(math.log(len(encodedString),2)))
    matrix_H = createHMatrix(numParityBits,len(encodedString))
    matrix_r = createRMatrix(encodedString)
    matrix_parity = np.matmul(matrix_H, matrix_r)
    parity_list = []
    for i in range(len(matrix_parity)):
        x = matrix_parity.item(i)
        parity_list.append(x%2)

    myBadBit = determineBadBit(parity_list)

    doubleError = determineDoubleError(encodedString,overallParity,myBadBit)
    if doubleError:
        #print("Two errors detected, abort this bit string")
        return [True, False, encodedString, None, None]

    if myBadBit:
        #print("there was an error at location " + str(myBadBit))
        newString = encodedString[0:myBadBit-1] + ("0" if encodedString[myBadBit-1] == "1" else "1") + encodedString[myBadBit:]
        #print("original bad string: " + encodedString)
        #print("corrected string: " + newString)
        recoveredMessage = recoverOriginalMessage(newString, numParityBits)
        #print("recovered message: " + recoveredMessage)
        return [False, True , newString, recoveredMessage, myBadBit]

    #print("no error occurred")
    #print("original and correct string: " + encodedString)
    recoveredMessage = recoverOriginalMessage(encodedString, numParityBits)
    #print("recovered message: " + recoveredMessage)
    return [False, False, encodedString, recoveredMessage, None]

# Simulator for wrong issues. 


def determineBadBit(parityList):
    parityList = parityList[::-1]
    bitstring = "".join([str(x) for x in parityList])
    decimalLocation = int(bitstring,2)
    #print("decimal location of bad bit: " + str(decimalLocation))
    return decimalLocation


def recoverOriginalMessage(encryptedString, k_num_parity_bits):
    encryptedList = list(encryptedString)
    indicesOfParity = set()
    for i in range(k_num_parity_bits):
        indicesOfParity.add((2**i)-1)
    recoveredList = [x for ind,x in enumerate(encryptedList) if ind not in indicesOfParity]
    recoveredString = "".join(recoveredList)
    #print("recovered string: " + recoveredString)
    return recoveredString
    

def determineDoubleError(hamString, parity_bit, badbit):
    counter = 0
    if parity_bit == "1":
        counter += 1
    counter += list(hamString).count("1")
    overallParity = True if counter%2 == 0 else False
    doubleError = overallParity and (badbit > 0)
    return doubleError

def createHMatrix(num_parity, lengthOfString):
    listOfLists = []

    for i in range(num_parity):
        #print("hi")
        tempList = []
        indexOfParity = (2**i)-1
        spacing = 2**i
        counter = 0
        place1 = True
        for j in range(indexOfParity):
            tempList.append(0)
            counter +=1 
        while counter < lengthOfString:
            for j in range(spacing):
                toAppend = 1 if place1 else 0
                tempList.append(toAppend)
                counter += 1
                if counter >= lengthOfString:
                    break
            place1 = not place1
        listOfLists.append(tempList)
    
    a = np.matrix(listOfLists)
    #print(a)
    #print(listOfLists)
    return(a)
    
def createRMatrix(hammingString):
    listOfLists = []
    for i in hammingString:
        x = [int(i)]
        listOfLists.append(x)
    a = np.matrix(listOfLists)
    #print(a)
    return a


