#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys, unicodedata, math, collections, random, time
from sets import Set

#reload(sys)
#sys.setdefaultencoding('utf8')

##------------------------------------------------------------------------------
##------------------CREATION OF CLEAN TEXT FOR EXPERIMENTATION------------------
##------------------------------------------------------------------------------

#Cleans a given text by removing not basic (a..z and white space) ascii characters
def cleanInputText(txt):
    unicoded = txt.decode('UTF-8', 'ignore')
    lowerCased = unicodedata.normalize('NFKD', unicoded.lower()).encode('ASCII', 'ignore')

    result = lowerCased.replace('\n','').replace('\r', ' ') \
            .replace('%', '').replace('$', '').replace('@', '').replace('&', '').replace('{', '').replace('}', '')\
            .replace('-', '').replace('<', '').replace('>', '').replace('(', '').replace(')', '').replace('_', '').replace('/', '') \
            .replace("'", '').replace('"', '').replace('#', '').replace(':', '').replace('*', '').replace('?', '').replace('¿', '') \
            .replace('.', '').replace(',', '').replace(';', '').replace('!', '').replace('¡', '').replace('[', '').replace(']', '')

    result = ''.join(i for i in result if not i.isdigit())      #Removing numbers...
    result = ' '.join(result.split())                           #Removing excess of white spaces

    return result


#Extracts the text from a file.
def readFromFile(filein):

    file = open(filein, 'r')
    contents = file.read()
    file.close()
    return contents


#Writes to file the given contents.
def writeToFile(fileOut, contents):

    f = open(fileOut, 'w+')
    f.write(str(contents))
    f.close()
    print ("Finished writing clean file")



##------------------------------------------------------------------------------
##---------------------------COMPUTATION OF ENTROPIES---------------------------
##------------------------------------------------------------------------------
#Given a text, returns its alphabet of symbols.
def getTextAlphabet(text):

    return list(Set(text))

#Prints the text alphabet.
def printTextAlphabet(text):

    print ('')
    alphabet = getTextAlphabet(text)
    print ("Source with " + str(len(alphabet)) + " letters. Alphabet of text:" )
    print (alphabet)

#Returns a single letter probability probability computed from given text.
def getSingleLetterProbability(letter, text):

    count = text.count(letter)
    return float(count)/len(text)

#Returns the symbols probabilities.
def getSymbolsProbabilities(text):

    probs = [] #Probabilities array
    alphabet = getTextAlphabet(text)

    for letter in alphabet:
        letterProb = getSingleLetterProbability(letter, text)
        probs.append(letterProb)

    return probs

#Returns the symbols probabilities in a dictionary to relate them to its letter.
def getSymbolsProbabilitiesAsDictionary(text):

    dictionary = {}
    alphabet = getTextAlphabet(text)
    for letter in alphabet:
        letterProb = getSingleLetterProbability(letter, text)
        dictionary[letter] = letterProb

    return dictionary

#Counts the number of appearances a pattern makes in a text
def countPatternAppearances(text, pattern):

    count = 0
    index = 0
    while True:
        index = text.find(pattern, index) + 1
        if(index > 0):
            count += 1
        else:
            return count

#Returns the joint probability of 2 letters
def getJointProbability(letterA, letterB, text):

    pattern = letterA + letterB
    count = countPatternAppearances(text, pattern)
    letterAAndLetterB = float(count)/(len(text) - 1)
    return letterAAndLetterB

#Computes the information given in a single probability
def computeInformation(probability):
    if probability == 0:
        return 0

    prob = math.log(probability, 2)
    return -prob

#Computes the entropy of a text
def getEntropy(text):
    #Given some probabilities...
    probs = getSymbolsProbabilities(text)

    #...We compute the entropy related to them
    ent = 0             #entropy
    for p in probs:
        ent = ent + p * computeInformation(p)
    return ent

#Computes the joit entropy
def getJointEntropy(text):

    alphabet = getTextAlphabet(text)
    ent = 0
    for l1 in alphabet:
        for l2 in alphabet:
            jointProb =  getJointProbability(l1, l2, text)
            ent += jointProb * computeInformation(jointProb)
    return ent

#Computes the conditional entropy
def getConditionalProbability(text, varLetter, knownLetter):

    jointProb = getJointProbability(knownLetter, varLetter, text)
    prob = (jointProb)/getSingleLetterProbability(knownLetter, text)
    return prob

#Computes the conditional entropy when knowing one letter
def getConditionalEntropyOfLetter(text, ltr):

    alphabet = getTextAlphabet(text)
    #P(A i B) / P(B) * P(A)
    ent = 0
    for varL in alphabet:
        prob = getConditionalProbability(text, varL, ltr)
        ent += prob * computeInformation(prob)
    return ent

#Computes conditional entropy of a text
def getConditionalEntropy(text):

    alphabet = getTextAlphabet(text)
    ent = 0
    for l1 in alphabet:
        for l2 in alphabet:
            jointProb = getJointProbability(l1, l2, text)
            condProb = getConditionalProbability(text, l2, l1)
            ent += jointProb * computeInformation(condProb)
    return ent

#Checks proposition H(X,Y) = H(X) + H(Y|X)
def checkProposition(text):

    jointE = getJointEntropy(text)
    simpleE = getEntropy(text)
    condE = getConditionalEntropy(text)

    print ('')
    print ("H(X,Y) = H(X) + H(Y|X)")
    print (str(jointE) + " = " + str(simpleE) + " + " + str(condE))
    sum = simpleE + condE
    print (str(jointE) + " = " + str(sum))

    print ('')
    print ("H(Y|X) <= H(Y)")
    print (str(condE) + " <= " + str(simpleE))



##------------------------------------------------------------------------------
##-----------------------------CREATION OF NEW TEXT-----------------------------
##------------------------------------------------------------------------------

#For this, we compute the frequencies and multiply each letter 100*freq and
#append this string of X times that letter to a global string.
#We then use the random function "choice" to select from that global string.
def createNewTextSameLetterFreq(text):

    #We use the length of the text as a multiplier to ensure that all letters appear at least 1 time in the generated random string
    multiplier = len(text)

    globalString = ""
    symbolsDict = getSymbolsProbabilitiesAsDictionary(text)
    for key in symbolsDict.keys():
        print ("Key: " + key + " Probability: " + str(int(symbolsDict[key] * multiplier)))
        globalString += (int(symbolsDict[key] * multiplier) * key)

    newText = ""
    for i in range(multiplier):
        newText += random.choice(globalString)

    return newText

#Creates new text with same joint and condition entropy of the given one.
def createNewTextSameJointEntropy(text):

    textLength = len(text)

    alphabet = getTextAlphabet(text)

    #Compute first letter
    simpleProbsDict = getSymbolsProbabilitiesAsDictionary(text)
    stringToChooseFrom = ""
    for key in simpleProbsDict.keys():
        stringToChooseFrom += (int(simpleProbsDict[key] * textLength) * key)

    newText = random.choice(stringToChooseFrom)


    lastLetter = newText[-1:]

    dictTimeStart = time.time()
    #Compute dictionary
    dictAllCondProbs = {}
    for l1 in alphabet:
        for l2 in alphabet:
            dictAllCondProbs[l1+l2] = getConditionalProbability(text, l2, l1)

    dictElapsedTime = time.time() - dictTimeStart

    print ("Dictionary of all conditional probabilities computed in " + str(dictElapsedTime) + " seconds")

    #Compute new text
    start_time = time.time()
    for i in range(textLength):
        dicProb = {}

        for letter in alphabet:
            dicProb[letter] = dictAllCondProbs[lastLetter + letter]

        stringToChooseFrom = ""
        for key in dicProb.keys():
            stringToChooseFrom += (int(dicProb[key] * textLength) * key)

        lastLetter = random.choice(stringToChooseFrom)
        newText += lastLetter

    elapsed_time = time.time() - start_time

    print ("Old text. Entropy: " + str(getEntropy(text)) + " Joint: " + str(getJointEntropy(text)) + " Conditional: " + str(getConditionalEntropy(text)))
    print ("New text. Entropy: " + str(getEntropy(newText)) + " Joint: " + str(getJointEntropy(newText)) + " Conditional: " + str(getConditionalEntropy(newText)))
    print ("Elapsed time: " + str(elapsed_time))
    return newText
