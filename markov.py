#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ngram model.
import codecs
import glob
import math
import pickle
import sys

from detectorBase import detectorBase 

#   Consider post processing, removing any key that has a character outside the
#   main script range, e.g., ASCII. Do the same for ASCII encodings such
#   as KNU.
ASCII_MIN = 0x0
ASCII_MAX = 0xff
ASCII_RANGE = [(ASCII_MIN, ASCII_MAX)]

# Unicode Burmese ranges
MYANMAR_SCRIPT_RANGES = [(0x1000, 0x109f), (0xAA60, 0xAA7f), (0xA9E0, 0xA9FF)]
BURMESE_INDEPENDENT_VOWELS = [(0x1021, 0x102a)]
BURMESE_CONSONANTS = [(0x1000, 0x1020), (0x103f)]
# BURMESE_CONSONANTS.extend(BURMESE_INDEPENDENT_VOWELS)
CONSONANTS_AND_IND_VOWELS = [(0x1000, 0x1020), (0x103f, 0x103f), (0x1021, 0x102a), (0x1075, 0x1081),
  (0x105a, 0x105d), (0x1061, 0x1061), (0x1065, 0x1066), (0x106e, 0x1070) ]
VARIANT_FORM0 = 0xfe00

SHAN_LETTER = [(0x1075, 0x1081)]
MON_LETTER = [(0x105a, 0x105d)]
KAREN_LETTER = [(0x1061, 0x1061), (0x1065, 0x1066), (0x106e, 0x1070)]  # SGAW, EASTERN, WESTERN

class markovModel(detectorBase):
  def __init__(self, lang, font, fileName=None):
    self.detectorType = 'MARKOV'
    self.lang = lang
    self.font = font
    self.model = {}  # Dictionary to hold
    self.probA = {}
    self.probBGivenA = {}
    self.ngramLength = 2
    self.numSamples = 0
    self.fileName = fileName
    self.modelFileName = ''
    self.linesAdded = 0
    self.totalNGram = 0
    self.logSum = 0.0  # Sum of log10 of nGrams fractions.

  def clearModel(self):
    self.model = {}
    
  def setN(self, n):
    self.ngramLength = n

  def buildModel(self, text):
    # Given the text sample, create ngrams.
    self.addToModel(text)

  def addToModel(self, text):
    # Create n-length sets.
    size = len(text)
    
    for keyTuple in self.getKeyTuple(text):
      A = keyTuple[0]
      B = keyTuple[1]
      if A in self.probA:
        self.probA[A] += 1
        if B in self.probBGivenA[A]:
          self.probBGivenA[A][B] += 1
          #print '  Incrementing %4x, %4x: %s' % (ord(A), ord(B), self.probBGivenA[A])
        else:
          self.probBGivenA[A][B] = 1
          #print '  Setting %4x with %4x: %s' % (ord(A), ord(B), self.probBGivenA[A])
      else: 
        self.probA[A] = 1
        self.probBGivenA[A] = {B : 1}
        #print '  New %4x with %4x: %s' % (ord(A), ord(B), self.probBGivenA[A])
     
      self.numSamples += 1

  def getKeyTuple(self, text):
  	# Find the next text starting with a Consonant or Independent Vowel.
    # Return that character and the following.
    # Don't skip the second, though.
    size = len(text)
    for i in xrange(size - 2):
      if inRanges(text[i], CONSONANTS_AND_IND_VOWELS):
        #print '(%4x %4x)' % (ord(text[i]), ord(text[i+1]))
        yield tuple(text[i:i+2])
        
  def addFileToModel(self):
    if self.fileName == None:
      return
    file = codecs.open(self.fileName, mode='r', encoding='utf-8')
    for line in file:
      self.addToModel(line)
      self.linesAdded += 1
    file.close()
    self.figureModelTotal()

  def figureModelTotal(self):
    total = 0
    self.logSum = 0.0
    for key in self.probA:
      total += self.probA[key]
      self.logSum += math.log(self.probA[key])
    self.totalNGram = total

  def pruneModelByASCII(self):
    # Remove model entries that have an ASCII character in the key.
    # Returns number of items and total count removed.
    return self.pruneModelByRange(ASCII_RANGE)

  def pruneModelByRange(self, rangeList):
    # Remove model entries that have a range of characters in the key.
    # Returns number of items and total count removed.
    itemsRemoved = 0
    countRemoved = 0
    keysToRemove = []
    for range in rangeList:
      exclude_min = range[0]
      exclude_max = range[1]
      for key in self.model:
        for char in key:
          ordChar = ord(char)
          if 0 <= exclude_min and ordChar <= exclude_max:
            keysToRemove.append(key)

    for key in keysToRemove:
      try:
        countRemoved += self.model[key]
        itemsRemoved += 1
        del self.model[key]
      except KeyError:
        continue  # Already gone
    self.figureModelTotal()
    return (itemsRemoved, countRemoved)

  def getKey2(self, item):
    return item[1]

  def countHistogram(self):
    # How many items with each count?
    histogram = {}
    for key in self.model:
      count = self.model[key]
      if count in histogram:
        histogram[count] += 1
      else:
        histogram[count] = 1
    sortedList = sorted([ [k,v] for k, v in histogram.items() ], key=self.getKey2)
    
    return sortedList
     
  def printModelStats(self):
    print 'Model file name = %s' % self.modelFileName
    print '  Last file processed = %s' % self.fileName
    print '  lang = %s, font = %s, ngram = %s' % (self.lang, self.font, self.ngramLength)
    print '  %d samples, %d lines, %d states, %d nGrams, sum(log(Ai)) = %f, factor=%f' % (
      self.numSamples, self.linesAdded, len(self.probA), self.totalNGram, self.logSum,
      (-self.logSum + len(self.probA) * math.log(self.totalNGram)))

  def getModelStats(self):
    result = {'modelName': self.modelFileName,
               'lastFileProcessed': self.fileName,
               'lang': self.lang,
               'font': self.font,
               'ngramSize': self.ngramLength,
               'samples': self.numSamples,
               'lines': self.linesAdded,
               'nGrams': len(self.model),
               'totalNGram': self.totalNGram,
               'logSum': self.logSum,
               }
    return result

  def printModelDetails(self):
    # Simple output of the counts.
    print '%d entries in model' % len(self.model)
    for key in self.probA.keys():
      print '(%4x): %d has %d entries' % (ord(key), self.probA[key], len(self.probBGivenA[key]),
       )
      for key2 in self.probBGivenA[key]:
        print '    (%4x): %d' % (ord(key2), self.probBGivenA[key][key2])

  def saveModel(self, saveFileName):
    file = codecs.open(saveFileName, 'wb')
    self.modelFileName = saveFileName
    pickle.dump(self, file)
    print 'Model of %d states saved to %s' % (len(self.probA), saveFileName)
    file.close()

  def rankText(self, intext):
    # Gets simple value of match of text to model.
    # Returns:
    #   match as fraction of model size
    #   raw match count
    matchCount = 0
    for keyTuple in self.getKeyTuple(intext):
      A = keyTuple[0]
      B = keyTuple[1]
      if A in self.probA:
        if B in self.probBGivenA[A]:
          count = self.probBGivenA[A][B]
          matchCount += count
    if matchCount > 0:
      #print 'MATCH = %d, totalNGram = %d, ratio = %f'  % (matchCount, self.totalNGram,
      #  float(matchCount) / self.totalNGram) 
      ratio = math.log(float(matchCount) / self.totalNGram)
    else:
      ratio = 0.0
    return (ratio, matchCount)


# Boolean indicating if a code point is in the list of ranges.
def inRanges(char, rangeList):
  for r in rangeList:
    if ord(char) >= r[0] and ord(char) <= r[1]:
      return True
  return False


# Gets a saved model.
def loadModel(fileName):
  try:
    fileIn = open(fileName, 'rb')
    result = pickle.load(fileIn)
    fileIn.close()
    return result
  except pickle.UnpicklingError:
    print '*Problem loading file %s' % fileName
    return None    


def getSavedModels(filenames):
  # Load saved models, printing out basic information.
  allModels = []
  for file in filenames:
    z3 = loadModel(file)
    allModels.append(z3)
  return allModels

 
def allModelStats(models):
  # Load saved models, printing out basic information.
  # Returns list of the models.
  for model in models:
    model.printModelStats()


# First attempt at detecting.
def tryMatch(modelList, testText, note): 
  bestRank = -10.0
  bestModel = None
  for model in modelList:
    (rank, raw) = model.rankText(testText)
    print '  model %s (%d), rank = %f, raw = %d' % (model.fileName, model.ngramLength, rank, raw)
    if rank > bestRank:
      bestRank = rank
      bestModel = model
  return (bestModel, bestRank)


def generateZawgyiModels():  
  zawgyiModel = markovModel('burmese', 'zawgyi', fileName='testdata/zawgi_VOA_samples.txt')
  for n in [2]:
    zawgyiModel.setN(n)
    zawgyiModel.clearModel()
    zawgyiModel.addFileToModel()
    zawgyiModel.saveModel('models/ZawgyiModel_%d_MM_model.save' % zawgyiModel.ngramLength)
    zawgyiModel.printModelStats()
    zawgyiModel.printModelDetails()

def generateSomeModels():   
  burmeseUnicodeModel = markovModel('burmese', 'unicode', fileName='testdata/burmeseUnicode.txt')
  for n in [2]:
    burmeseUnicodeModel.setN(n)
    burmeseUnicodeModel.clearModel()
    burmeseUnicodeModel.addFileToModel()
    burmeseUnicodeModel.saveModel('models/UnicodeBurmese_Model_%d_MM_model.save' % burmeseUnicodeModel.ngramLength)
    burmeseUnicodeModel.printModelStats()
    burmeseUnicodeModel.printModelDetails()
  
  monKoaModel = markovModel('mon', 'monkoa', fileName='testdata/Mon_kaowao.txt')
  for n in [2]:
    monKoaModel.setN(n)
    monKoaModel.clearModel()
    monKoaModel.addFileToModel()
    monKoaModel.saveModel('models/MonKoaModel_%d_MM_model.save' % monKoaModel.ngramLength)
    monKoaModel.printModelStats()

  shanModel = markovModel('shan', 'unicode', fileName='testdata/shanUnicode.txt')
  for n in [2]:
    shanModel.setN(n)
    shanModel.clearModel()
    shanModel.addFileToModel()
    shanModel.saveModel('models/shanUnicode_%d_MM_model.save' % shanModel.ngramLength)
    shanModel.printModelStats()
    shanModel.printModelDetails()

def generateMonUniModels():  
  monModel = markovModel('mon', 'unicode', fileName='testdata/monUnicode.txt')
  for n in [2]:
    monModel.setN(n)
    monModel.clearModel()
    monModel.addFileToModel()
    monModel.saveModel('models/monUnicode_%d_MM_model.save' % monModel.ngramLength)
    monModel.printModelStats()

def generateKarenUniModels():  
  newModel = markovModel('karen', 'unicode', fileName='testdata/Karen.txt')
  for n in [2]:
    newModel.setN(n)
    newModel.clearModel()
    newModel.addFileToModel()
    newModel.saveModel('models/karenUnicode_%d_MM_model.save' % newModel.ngramLength)
    newModel.printModelStats()

  newModel = markovModel('karen', 'zwebakin', fileName='testdata/Zwebakin.txt')
  for n in [2]:
    newModel.setN(n)
    newModel.clearModel()
    newModel.addFileToModel()
    newModel.saveModel('models/karenZwebakin_%d_MM_model.save' % newModel.ngramLength)
    newModel.printModelStats()


def generateAllModels():
  generateSomeModels()
  generateMonUniModels()
  generateKarenUniModels()
  generateZawgyiModels()               


def main(argv=None):
  generateAllModels()
  #generateZawgyiModels()
  #generateSomeModels()

  filenames = glob.glob('models/*MM_model.save')
  print 'Found %d saved models: %s' % (len(filenames), filenames)
  allModels = getSavedModels(filenames)
  print '%d models found' % len(allModels)
  print 'MODELS = %s' % allModels
  # Statistics on saved models:
  # allModelStats(allModels)

  return
  
  # Try removing ASCII from the models.
  for model in allModels:
    print 'MODEL = %s' % model
    (result1, result2) = model.pruneModelByASCII()
    print 'Removed %d items and %d states ' % (result1, result2)
    print model.printModelStats()


if __name__ == "__main__":
    sys.exit(main(sys.argv))