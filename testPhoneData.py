#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

import logging
import os 
import re
import sys

import transliterate
import translit_myazedi
import translit_zawgyi

# Test data from phone company, comparing their conversion with mine.

class testOtherConverter():

  def __init__(self):
    self.zToU = transliterate.Transliterate(
        translit_zawgyi.ZAWGYI_UNICODE_TRANSLITERATE,
        translit_zawgyi.ZAWGYI_description)
    self.data = []
  
  def readTestData(self, tsvFile):
    print 'tsvFile = %s' % tsvFile
    with open(tsvFile,'rb') as tsvin:
      tsvreader = csv.reader(tsvin, delimiter='\t')
      print 'input file %s' % tsvreader
      rowNum = 0

      for row in tsvreader:
        self.data.append(row)
        # print '** Row %d: %s vs. %s' % (rowNum, row[1], row[2])
        rowNum += 1
		
  def runComparisons(self, filenameOut):
    print '** Transliterator %s' % self.zToU.description
    rowNum = 0
    numDiffs = 0
    numSame = 0
    with open(filenameOut, 'wb') as csvfile:
      outWriter = csv.writer(csvfile, delimiter='\t',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
      # Header
      outWriter.writerow(['Comparison', 'Zawgyi test', 'test conversion', 'cwc conversion'])
      for row in self.data:
        # print row
        print 'ROW %d: %s' % (rowNum, row[1])
        uOutput = self.zToU.transliterate(row[1])
        if uOutput == row[1]:
          print 'Row %d: Converted the same as input' % rowNum
        if uOutput != row[2]:
          print 'difference at row %d' % rowNum
          print '  >> %s' % uOutput
          print '  $$ %s' % row[2]
          numDiffs += 1
          outWriter.writerow(['DIFFERENT', row[1], row[2], row[3], uOutput])
        else:
          numSame += 1
          outWriter.writerow(['SAME', row[1], row[2], row[3], uOutput])
        rowNum += 1
        
    print 'NumDiffs = %d, numSame = %d' % (numDiffs, numSame)
 
def main(argv=None):

  testData = testOtherConverter()
  dirPath = os.path.dirname(os.path.realpath(__file__))
  filename = 'testdata/samples.tsv'
  filePath = os.path.join(dirPath, filename)
  print filePath
  if os.path.exists(filePath):
    testData.readTestData(filePath)
  else:
    print 'File %s does not exist' % filePath

  testData.runComparisons('testout.tsv')

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))