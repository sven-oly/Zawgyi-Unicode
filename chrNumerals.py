#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Working 28-Mar-2016. All tests pass.

import logging
import re
import sys
import types

# For internationalization
from django.utils.translation import ugettext as _
from django.conf import settings



reducers = [100, 1000, 1e6, 1e9, 1e12, 1e15, 1e18]

numeralValues = [1e18, 1e15, 1e12, 1e9, 1e6, 1000,
    100, 90, 80, 70, 60, 50, 40, 30, 20,
    19, 18, 17, 16, 15, 14, 13, 12, 11, 10,
    9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    
imageNames = ['1000000000000000000', '1000000000000000', '1000000000000',
  '1000000000', '1000000','1000', '100',
  '90', '80', '70', '60', '50', '40', '30',
  '20', '19', '18', '17', '16', '15', '14',
  '13', '12', '11', '10',
  '9', '8', '7', '6', '5', '4', '3',
  '2', '1', '0']
fractionName = 'fract'

chr_digital_map = {}

# Process the input numeral, outputting a list of count and numerals.
def digitalToSequoah(decimalNum):

  # Returns a list of (value) of the decoded number in Sequoyah's numerals
  result = []
  resultImage = []

  if decimalNum == 0:
    result = [0]
    resultImage = ['0']
    return (result, resultImage)

  if decimalNum < 0:
    remaining = -decimalNum
    result.append(-1)
    resultImage = ['-1']
  else:
    remaining = decimalNum

  index = 0
  count = 0
  # TODO: handle fractions.
  while remaining > 0 and index < len(numeralValues) and count < 100:
    if remaining > 0 and remaining < 1:
      resultImage.append(fractionName)
      result.append(-10)  # Flag for fraction
      break;
        
    if remaining >= numeralValues[index]:
      #logging.info(' index: %d, value[index]: %d, count: %d' % (index, numeralValues[index], count))
      count = int(remaining / numeralValues[index])
      remaining -= count * numeralValues[index]
    if count > 0:
      if count == 1:
        resultImage.append(imageNames[index])
        result.append(numeralValues[index])
      else:
        prefix = digitalToSequoah(count)
        if list(prefix):
          resultImage.extend(prefix[1])
          result.extend(prefix[0])
        else:
          resultImage.append(prefix[1])
          result.append(int(prefix[0]))
        resultImage.append(imageNames[index])
        result.append(numeralValues[index])
      #logging.info('  result = %s' % (numeralValues[index]))
    count = 0
    index += 1

  #logging.info('CHR version = %s' % resultImage)
  #logging.info('CHR result  = %s' % result)
  return (result, resultImage)  # Both the numbers and the strings.

# Set up the map.
def setUpMap():
  global chr_digital_map
  for index in range(len(imageNames)):
    chr_digital_map[imageNames[index]] = numeralValues[index]

def cleanUpListDeletions(l1, l2):
  # Remove items where l1[i] == -1.
  i = len(l1) - 1
  while i >= 0:
    if l1[i] == -1:
      del l1[i]
      del l2[i]
    i -= 1
      
def numListToInteger(numList):
  working = numList[:]
  tags = numList[:]
  #logging.info('** Starting:   %s' % working)

  # a. scan for add small
  start = 0
  limit = len(working)
  sum = 0
  while start < limit:
    end = start
    while end < limit and working[end] < 100:
      sum += working[end]
      end += 1
    if end > start:
      working[start] = sum
      for i in range(start + 1, end):
        tags[i] = -1  # to be removed
      sum = 0
    start += 1
  cleanUpListDeletions(tags, working)
  #logging.info('** Small added: %s' % working)
            
  # b. scan for multiply hundreds
  start = 1
  limit = len(working)
  while start < limit:
    if working[start - 1] < 100 and working[start] == 100:
      working[start] = working[start - 1] * working[start]
      tags[start-1] = -1
    start += 1
  cleanUpListDeletions(tags, working)
  #logging.info('** 100 times: %s' % working)    

  # c. scan for add to hundreds
  start = 1
  limit = len(working)
  while start < limit:
    if tags[start - 1] == 100 and tags[start] < 100:
      working[start] = working[start - 1] + working[start]
      tags[start-1] = -1
    start += 1
  cleanUpListDeletions(tags, working)
  # logging.info('** 100s added: %s' % working)    

  # d. scan for multiply 10^N
  start = 1
  limit = len(working)
  while start < limit:
    if tags[start - 1] <= 100 and tags[start] > 100:
      working[start] = working[start - 1] * working[start]
      tags[start-1] = -1
    start += 1
  cleanUpListDeletions(tags, working)
  #logging.info('** 10^N times: %s' % working)         

  grandSum = 0
  for x in working:
    grandSum += x
  return grandSum

# Take a string of codes in text, converting to values, eventually to one integer.
def processCodes(codes):
  global chr_digital_map
  if len(chr_digital_map) == 0:
    setUpMap()

  # Remove brackets and spaces.
  t1 = codes.replace('[', '', 1).replace("'", '').replace(']', '').replace(' ', '')
  # Split by ","
  chr_list = t1.split(',')
  dec_list = []

  # Convert each to a digital value
  for c in chr_list:
    # TODO: Handle out of range.
    if c in chr_digital_map:
      v = chr_digital_map[c]
    else:
      v = -1
    dec_list.append(v)

  numericValue = numListToInteger(dec_list)
  return numericValue

# -------------------------------------------------------------------------------
# Runs tests to verify correct behavior
chrTestSets = (	
  [[0], 0],
  [[1, 1], 2],
  [[20,2], 22],
  [[4, 100, 8], 408],
  [[30, 1000, 7, 100, 50, 6], 30756],
  [[3, 100, 7], 307],
  [[100, 70, 9, 1000], 179000],
  [[6, 1000, 6, 100, 60, 6], 6666],
  [[50, 8, 1000, 40], 58040],
  [[100, 2, 1e6, 3, 1000, 4, 100, 50, 6], 102003456],
  [[17, 1e12, 8, 1000, 1], 17000000008001],
  [[1e9, 20, 1e6, 30, 4, 1000, 5, 100, 60, 7], 1020034567],
  [[7, 1000000000000, 20, 1, 1000000000, 30, 2, 1000000, 30, 9, 1000, 5, 100, 60, 7],
    7021032039567],
  [[9, 1e12, 9, 100, 80, 7, 1e3, 30], 9000000987030], 
  [[20, 3, 1000, 4], 23004]
  )

# Tests num lists to integers.
def testChrToDec():
  failCount = 0
  passCount = 0

  resultList = []
  for test in chrTestSets:
    result = numListToInteger(test[0])
    if result == test[1]:
      passCount += 1
      resultStatus = 'PASS'
    else:
      failCount += 1
      resultStatus ='FAIL'
    resultList.append([resultStatus, test, result])

  return ('Test CHR to Dec', (passCount, failCount), resultList)

# Tests integers to num lists.

def testDecToChr():
  failCount = 0
  passCount = 0

  resultList = []
  for test in chrTestSets:
    result = digitalToSequoah(int(test[1]))[0]
    if result == test[0]:
      passCount += 1
      resultStatus = 'PASS'
    else:
      failCount += 1
      resultStatus ='FAIL'
    resultList.append([resultStatus, test, result])

  return ('Test decimal to CHR', (passCount, failCount), resultList)
