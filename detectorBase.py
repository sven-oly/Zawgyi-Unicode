#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import glob
import math
import pickle
import sys

# Detector base class.

class detectorBase(object):
  def __init__(self):
    self.lang = lang
    self.font = font
    self.detectorType = None
    self.model = {}  # Dictionary to hold
    self.numSamples = 0
    self.fileName = fileName
    self.modelFileName = ''
    self.linesAdded = 0
