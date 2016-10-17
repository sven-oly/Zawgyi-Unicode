#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ngram model.
import codecs
import glob
import math
import pickle
import sys

from detectorBase import detectorBase 

#   Do post processing, removing any key that has a character outside the
#   main script range, e.g., ASCII. Do the same for ASCII encodings such
#   as KNU.
ASCII_MIN = 0x0
ASCII_MAX = 0xff
ASCII_RANGE = [(ASCII_MIN, ASCII_MAX)]

# Burmese ranges
MYANMAR_SCRIPT_RANGES = [(0x1000, 0x109f), (0xAA60, 0xAA7f), (0xA9E0, 0xA9FF)]

class ngramModel(detectorBase):
  def __init__(self, lang, font, fileName=None):
    self.detectorType = 'NGRAM'
    self.lang = lang
    self.font = font
    self.model = {}  # Dictionary to hold
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
      if keyTuple in self.model:
        self.model[keyTuple] += 1
      else: 
        self.model[keyTuple] = 1
      self.numSamples += 1

  def getKeyTuple(self, text):
    # Generator function that creates ngrams from the piece of text.
    size = len(text)
    for i in xrange(size - self.ngramLength + 1):
      indexList = []
      for j in range(i, self.ngramLength + i):
        indexList.append(text[j])
      yield tuple(indexList)
        
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
    samples = 0
    for key in self.model:
      total += self.model[key]
      self.logSum += math.log(self.model[key])
    self.totalNGram = total

  def pruneModelByASCII(self):
    # Remove model entries that have an ASCII character in the key.
    # Returns number of items and total count removed.
    return self.pruneModelByRange(ASCII_RANGE)

  def removeKeys(self, keysToRemove):
    # Get rid of keys in the list.
    # Returns (count of items removed, total values removed)
    itemsRemoved = 0
    countRemoved = 0
    for key in keysToRemove:
      try:
        countRemoved += self.model[key]
        itemsRemoved += 1
        del self.model[key]
      except KeyError:
        continue  # Already gone
    self.figureModelTotal()
    return (itemsRemoved, countRemoved)
  
  def quantizeByN(self, f):
    # Remove model entries with fractional counts less than f.
    # Returns number of items and total count removed.
    keysToRemove = []
    N = f * self.totalNGram
    for key in self.model:
      if self.model[key] < N:
        keysToRemove.append(key)
    return self.removeKeys(keysToRemove)
   
  def pruneModelByRange(self, rangeList):
    # Remove model entries that have a range of characters in the key.
    # Returns number of items and total count removed.
    keysToRemove = []
    for range in rangeList:
      exclude_min = range[0]
      exclude_max = range[1]
      for key in self.model:
        for char in key:
          ordChar = ord(char)
          if 0 <= exclude_min and ordChar <= exclude_max:
            keysToRemove.append(key)
    return self.removeKeys(keysToRemove)

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
    print '  %d samples, %d lines, %d states, %d nGrams, sum(log(Ai)) = %f, factor=%8.1f' % (
      self.numSamples, self.linesAdded, len(self.model), self.totalNGram, self.logSum,
      (-self.logSum + len(self.model) * math.log(self.totalNGram)))

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
    for key in self.model.keys():
      print key, self.model[key]

  def saveModel(self, saveFileName=None):
    if saveFileName == None:
      saveFileName = self.modelFileName
    file = codecs.open(saveFileName, 'wb')
    self.modelFileName = saveFileName
    pickle.dump(self, file)
    print 'Model of %d states saved to %s' % (len(self.model), saveFileName)
    file.close()

  def rankText(self, intext):
    # Gets simple value of match of text to model.
    # Returns:
    #   match as fraction of model size
    #   raw match count
    matchCount = 0
    for keyTuple in self.getKeyTuple(intext):
      if keyTuple in self.model:
        count = self.model[keyTuple]
        matchCount += count
    if matchCount > 0:
      #print 'MATCH = %d, totalNGram = %d, ratio = %f'  % (matchCount, self.totalNGram,
      #  float(matchCount) / self.totalNGram) 
      ratio = math.log(float(matchCount) / self.totalNGram)
    else:
      ratio = -100.0
    return (ratio, matchCount)


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
  zawgyiModel = ngramModel('burmese', 'zawgyi', fileName='testdata/zawgi_VOA_samples.txt')
  for n in [2, 3, 4, 5]:
    zawgyiModel.setN(n)
    zawgyiModel.clearModel()
    zawgyiModel.addFileToModel()
    zawgyiModel.saveModel('models/ZawgyiModel_%d_model.save' % zawgyiModel.ngramLength)
    zawgyiModel.printModelStats()

def generateSomeModels():   
  burmeseUnicodeModel = ngramModel('burmese', 'unicode', fileName='testdata/burmeseUnicode.txt')
  for n in [2, 3, 4, 5]:
    burmeseUnicodeModel.setN(n)
    burmeseUnicodeModel.clearModel()
    burmeseUnicodeModel.addFileToModel()
    burmeseUnicodeModel.saveModel('models/UnicodeBurmese_Model_%d_model.save' % burmeseUnicodeModel.ngramLength)
    burmeseUnicodeModel.printModelStats()
  
  monKoaModel = ngramModel('mon', 'monkoa', fileName='testdata/Mon_kaowao.txt')
  for n in[ 2, 3, 4, 5]:
    monKoaModel.setN(n)
    monKoaModel.clearModel()
    monKoaModel.addFileToModel()
    monKoaModel.saveModel('models/MonKoaModel_%d_model.save' % monKoaModel.ngramLength)
    monKoaModel.printModelStats()

  shanModel = ngramModel('shan', 'unicode', fileName='testdata/shanUnicode.txt')
  for n in[ 2, 3, 4, 5]:
    shanModel.setN(n)
    shanModel.clearModel()
    shanModel.addFileToModel()
    shanModel.saveModel('models/shanUnicode_%d_model.save' % shanModel.ngramLength)
    shanModel.printModelStats()

def generateMonUniModels():  
  monModel = ngramModel('mon', 'unicode', fileName='testdata/monUnicode.txt')
  for n in[ 2, 3, 4, 5]:
    monModel.setN(n)
    monModel.clearModel()
    monModel.addFileToModel()
    monModel.saveModel('models/monUnicode_%d_model.save' % monModel.ngramLength)
    monModel.printModelStats()

def generateKarenUniModels():  
  newModel = ngramModel('karen', 'unicode', fileName='testdata/Karen.txt')
  for n in[ 2, 3, 4, 5]:
    newModel.setN(n)
    newModel.clearModel()
    newModel.addFileToModel()
    newModel.saveModel('models/karenUnicode_%d_model.save' % newModel.ngramLength)
    newModel.printModelStats()

  newModel = ngramModel('karen', 'zwebakin', fileName='testdata/Zwebakin.txt')
  for n in[ 2, 3, 4, 5]:
    newModel.setN(n)
    newModel.clearModel()
    newModel.addFileToModel()
    newModel.saveModel('models/karenZwebakin_%d_model.save' % newModel.ngramLength)
    newModel.printModelStats()


def generateAllModels():
  generateSomeModels()
  generateMonUniModels()
  generateKarenUniModels()
  generateZawgyiModels()               


def main(argv=None):
  generateAllModels()

  filenames = glob.glob('models/*.save')
  print 'Found %d saved models: %s' % (len(filenames), filenames)
  allModels = getSavedModels(filenames)
  print '%d models found' % len(allModels)
  print 'MODELS = %s' % allModels
  # Statistics on saved models:
  # allModelStats(allModels)

  # Try removing ASCII from the models.
  for model in allModels:
    print '---------------\nMODEL = %s' % model
    print model.printModelStats()
    (result1, result2) = model.pruneModelByASCII()
    print '  ASCII: Removed %d states and %d nGramTotal' % (result1, result2)
    print model.printModelStats()
    
    # Reduce if the count is small.
    minFraction = 0.0003
    print '  Remove all less than %8.5f.' % (minFraction)
    (result1, result2) = model.quantizeByN(minFraction)
    print '  FRACTION Removed %d states and %d nGramTotal' % (result1, result2)
    # print model.printModelStats()
    # model.saveModel()


if __name__ == "__main__":
    sys.exit(main(sys.argv))