#!/usr/bin/python
# -*- coding: UTF-8 -*-
import EntropyUtils
import sys, getopt

class STATIC_VARS:
    EXPECTED_NUM_OF_ARGS = 4;


#Outputs usage for user
def usage():
    print ('Usage: tester.py -i <inputfile> -o <outputfile>')
    sys.exit(2)

#Main function
def main(argv):

    if len(argv) < STATIC_VARS.EXPECTED_NUM_OF_ARGS:
        usage()

    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        usage()

    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ("-i", "--ifile"):
            filein = arg
        elif opt in ("-o", "--ofile"):
            fileout = arg

    print ("Reading from file " + filein)
    contents = EntropyUtils.readFromFile(filein)

    print ("Cleaning text...")
    result = EntropyUtils.cleanInputText(contents)

    print ("Writing clean text to " + fileout)
    EntropyUtils.writeToFile(fileout, result)

    EntropyUtils.printTextAlphabet(result)

    print ('')
    print ("Entropy: ")
    print (EntropyUtils.getEntropy(result))

    print ('')
    print ("Joint entropy: ")
    print (EntropyUtils.getJointEntropy(result))


    #First letter, for testing purposes
    letter = EntropyUtils.getTextAlphabet(result)[0]

    print ('')
    print ("Conditional entropy of letter " + letter)
    print (EntropyUtils.getConditionalEntropyOfLetter(result, letter))

    print ('')
    print ("Checking proposition...")
    EntropyUtils.checkProposition(result)

    print ('')
    print ('Creating new texts...')
    newText = EntropyUtils.createNewTextSameLetterFreq(result)
    newTextJoint = EntropyUtils.createNewTextSameJointEntropy(result)

    EntropyUtils.writeToFile(fileout + "_new_simple_text", newText)
    EntropyUtils.writeToFile(fileout + "_new_complex_text", newTextJoint)


if __name__ == "__main__":
   main(sys.argv[1:])
