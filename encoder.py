#Encode a byte string with parity bits 
import math
import numpy as np

def determineNumBits(stringLength):
    lowerK = int(math.ceil(math.log(stringLength,2)))
    print(lowerK)

    while 2**lowerK < stringLength + lowerK + 1:
        print("doing it ")
        lowerK += 1
    
    return lowerK

def encoder(bitString):
    print(len(bitString))

    numParityBits = determineNumBits(len(bitString))
    bitStringList = list(bitString)
    for i in range(numParityBits):
        bitStringList.insert((2**i)-1,'p'+str(i+1))

    print(bitStringList)

    def evaluateParity(p_index, space):

        print("space " + str(space))
        print("pindex " + str(p_index))
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
    toPrintList = []
    for i in range(numParityBits):
        indexOfParity = (2**i)-1
        toPrintList.append(bitStringList[indexOfParity])
    print(toPrintFinal)
    print(toPrintList)


def decoder(encodedString):
    numParityBits =  int(math.ceil(math.log(len(encodedString),2)))
    matrix_H = createHMatrix(numParityBits,len(encodedString))
    matrix_r = createRMatrix(encodedString)
    matrix_parity = np.matmul(matrix_H, matrix_r)
    parity_list = []
    for i in range(len(matrix_parity)):
        x = matrix_parity.item(i)
        parity_list.append(x%2)
    myBadBit = determineBadBit(parity_list)
    if myBadBit:
        print("there was an error at location " + str(myBadBit))
        newString = encodedString[0:myBadBit-1] + ("0" if encodedString[myBadBit-1] == "1" else "1") + encodedString[myBadBit:]
        print(encodedString[0:myBadBit-1])
        print(encodedString)
        print(newString)
        return newString
    print("no error occurred")
    return(encodedString)
    #print(parity_list)
    #print(matrix_parity)

# What is it mean if one of the parity bits is messed up?
# Convert a encoded and corrected string back to just the bare corrected string
# Double error detecting?
# Simulator for wrong issues. 


def determineBadBit(parityList):
    parityList = parityList[::-1]
    bitstring = "".join([str(x) for x in parityList])
    decimalLocation = int(bitstring,2)
    print(decimalLocation)
    return decimalLocation




def createHMatrix(num_parity, lengthOfString):
    listOfLists = []

    for i in range(num_parity):
        print("hi")
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
    print(a)
    print(listOfLists)
    return(a)
    
def createRMatrix(hammingString):
    listOfLists = []
    for i in hammingString:
        x = [int(i)]
        listOfLists.append(x)
    a = np.matrix(listOfLists)
    print(a)
    return a


    
#createRMatrix("10101010101010")
decoder('0100011')

def test():
    if 1:
        print("hihi")
    
test()

        
            













    








    #toPrint  = "".join(bitStringList)
    #print(toPrint)



#encoder("100010100110000110100111")
#encoder("01010101010101010101010101010101")



    




# determineNumBits(244)
# determineNumBits(32)
# determineNumBits(100)
    