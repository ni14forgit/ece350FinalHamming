import random
import encoder
def generateIssue(encodedString, indices):
    for i in indices:
        x = int(i) -1 
        encodedString = encodedString[:x] + ("0" if encodedString[x] == "1" else "1") + encodedString[x+1:]
    return encodedString

def generateInformation(numBits):
    # if predefinedInfo:
    #     return predefinedInfo
    bitString = ""
    for i in range(numBits):
        bitString += ("1" if (random.randint(0,1) == 1) else "0")
    return bitString

def userInputFirst(x):
    error = False
    nums = "23456789"
    length = x[1:]

    bigNumberInX = False
    for i in nums: 
        if i in x:
            bigNumberInX = True

    if not x:
        #print("No input detected")
        return(None, True, "No input detected")


    if "R" not in x and bigNumberInX and x.isdigit():
        #print("can only include 1s and 0s in a bit string, please redo")
        return(None, True, "can only include 1s and 0s in a bit string, please redo")
    
    if "R" in x and not length.isdigit():
        #print("make sure R is only included once, could not convert: " + length)
        return(None, True, "make sure R is only included once, could not convert: " + length)
    
    if "R" in x: 
        val = generateInformation(int(length))
    else: 
        val = x 
    
    return (val, False, "correct input!")
    

def userInputSecond(x, passString):

    if not x: 
        return(x, False, "No bits are corrupted!")

    if not x.isdigit():
        return(None, True, "Please do not include letters as an index")

    for i in x:
        if int(i) > len(passString):
            return (None, True, "Make sure indices are within range")


    if len(x) > 2: 
        return(x, False, "More than 2 indices were chosen, but will still continue simulation")

    return (x, False, "Selected " + str(len(x)) + " indices to flip!")



def simulator():
    print("Welcome to the Hamming Simulator!")
    print("We will be encoding and decoding strings - and detecting errors!")
    print("\n")
    while True: 
        print("If you would like to type in your own custom bitstring, please do so.")
        print("Otherwise, type R and enter a bitstring length and we'll randomly create one for you.")
        print("ex: R25 or 10011010101110001")
        inputerror = True
        value = ""
        while inputerror:
            x = input()
            [value, inputerror, message] = userInputFirst(x)
            if inputerror: 
                print(message)
                print("Enter once again: ")
        print("Your created bit string: " + value)
        [encodedString, overallParity, parityBits] = encoder.encoder(value)
        print("Encoded Hamming String: " + encodedString)
        print("Parity bits created: " + str(parityBits))
        print("Overall parity bit for Double Error Detection: " + overallParity)
        print("\n")
        print("Please indicate 0 to 2 indices to flip bits")
        print("ex: 47 -> flips the fourth and seventh bit")
        print("ex: 1 -> flips the first bit")
        print("ex: (Enter) -> Does not change any bit")
        inputerror = True
        while inputerror:
            x = input()
            [value, inputerror, message] = userInputSecond(x, encodedString)
            print(message)
            if inputerror:
                print("Enter once again: ")
        print("Original String: " + encodedString)
        potentiallyCorrupted = generateIssue(encodedString, value)
        print("Potentially Corrupted String: " + potentiallyCorrupted)
        print("\n")
        print("Beginning Decryption")
        [doubleError, SingleError, hammingMessage, rawMessage, badbit] = encoder.decoder(potentiallyCorrupted, overallParity)
        if doubleError:
            print("Double error detected! Abort")
        elif SingleError:
            print("Single error detected at location " + str(badbit))
            print("Original correct hamming: " + hammingMessage)
            print("Original raw message: " + rawMessage)
        else:
            print("No error detected")
            print("Original correct hamming: " + hammingMessage)
            print("Original raw message: " + rawMessage)
        print("\n")
        print("thank you, if you would like to try other bitstrings, press r")
        x = input()
        if "r" not in x:
            return
        print("\n")

simulator()





            







