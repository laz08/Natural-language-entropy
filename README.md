# Natural language entropy study

## About

This little project is product of a class assignment, coded around February 2016.

It is composed only by two files:

* __EntropyUtils.py__, which is the core and has all the important methods.
* __tester.py__, which allows a direct route to use the methods defined in __EntropyUtils.py__
from the terminal.


## How it works
Although briefly done, almost every method defined in __EntropyUtils__ is explained above its header.

The most interesting functions are stated here.

### Clean text

* _cleanInputText(text)_ cleans an input text so that it does not have special characters.

### Entropies computation

* _getEntropy(text)_ computes the entropy for a variable X whose values are letters from a given text. That is, __H(X)__.
* _getJointEntropy(text)_ computes the joint entropy of a pair of vars: X, Y. That is, __H(X, Y)__.
* _getConditionalEntropyOfLetter(text)_ computes the entropy of a variable Y, where its value is a random letter from the given text. That is, __H(Y|x[i])__.
* _getConditionalEntropy(text)_ computes the conditional entropy of two variables from the given text. That is,  __H(X|Y)__.

You can also check the functions using _checkProposition(text)_.

### New texts creator

You can create two (random) texts taking the given text as an example:

* _createNewTextSameLetterFreq(text)_, creates a text with the same letters' frequencies as the original text.
* _createNewTextSameJointEntropy(text)_, creates a text with the same joint entropy as the original text.
