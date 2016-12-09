#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Composite ngram model. Contains ngrams from several models. Used to evaluate which one
# fits best.

import codecs
import glob
import math
import pickle
import sys

class compositeNgramModel(detectorBase):
  def __init__(self, lang, font, fileName=None):
    self.detectorType = 'NGRAM'
    self.models = []  # info on the component models
    self.model = {}  # Dictionary to hold keys and the counts for each model.
    self.logSum = 0.0  # Sum of log10 of nGrams fractions.
    
# Each item in the model dictionary will hold the counts of each model for that ngram.

# The idea is that the matching for each string will only need to look up each ngram once,
# summing for each of the models. Then the results are normalized
