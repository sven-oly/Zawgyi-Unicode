#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

from collections import defaultdict  # available in Python 2.5 and newer
import difflib

import codecs
import json
import logging
import os
import re
import urllib
import webapp2

from google.appengine.ext.webapp import template

# For internationalization
from django.utils.translation import ugettext as _
from django.conf import settings

# Compare Zawgyi and Unicode, side by side.

class compareHandler(webapp2.RequestHandler):
  def get(self):
    # read the files

    path = os.path.join(os.path.split(__file__)[0], 'CLDR/my_Qaaz.xml')
    fZ = codecs.open(path, encoding='utf-8')
    docZ = fZ.read()
    fZ.close()

    path = os.path.join(os.path.split(__file__)[0], 'CLDR/my.xml')
    fU = codecs.open(path, encoding='utf-8')
    docU = fU.read()
    fU.close()

    docZ = docZ.split('\n')
    docU = docU.split('\n')

    print(len(docZ),len(docU))

    print(docZ)
    pairs = []

    for i in xrange(min(len(docZ),len(docU), 200)):
      tuple = [docZ[i].encode('utf-8'),
               docU[i].encode('utf-8')]
      pairs.append(tuple)

    print('%s pairs' % len(pairs))
    print('pairs = %s' % pairs)

    # create SxS for JS

    # Expect that we have files that are the same content on each line, but
    # different encoding.

    template_values = {
        'description': 'Burmese CLDR',
        'encodingFonts': ['ZawgyiOne', 'NotoSansMyanmar'],
        'pairs': pairs,
    }

    path = os.path.join(os.path.dirname(__file__), 'comparetext.html')
    self.response.out.write(template.render(path, template_values))

    return


# Compare columns of a given spreadsheet
class compareColumnsHandler(webapp2.RequestHandler):
  def get(self):
    # read the file

    filename = 'Copy of Zawgyi detector%2Fconverter comp_ 20180709 top 10k queries - query.20180709.10k.cpp_js.tsv'
    print('INPUT FILE = %s' % filename)
    path = os.path.join(os.path.split(__file__)[0], 'CONVERTER_COMPARE', filename)
    fZ = codecs.open(path, encoding='utf-8')
    column_data = fZ.readlines()
    fZ.close()

    d = difflib.Differ()  # For comparing lines

    print('** %s rows found ' % len(column_data))

    my_char_pattern = re.compile(ur'[\u1000-\u109f]+')
    nya_pattern = re.compile(ur'\u1009')
    space_pattern = re.compile(ur'([\s\u200b]+)')
    ra_e_pattern = re.compile(ur'\u1031([\u1000-\u102a])\u103c')
    ra_sub_pattern = re.compile(ur'\u103c\u1039([\u1000-\u102a])')

    fffd_pattern = re.compile(ur'\ufffd')
    digit0_pattern = re.compile(ur'\u1040')
    digit4_pattern = re.compile(ur'\u1044')

    colZ = 0  # Zawgyi input
    colU1 = 3  # C++ converter result
    colU2 = 7  # JS converter

    pattern_counts = defaultdict(int)

    groups = []
    for i in xrange(min(len(column_data), 250)):
      if my_char_pattern.search(column_data[i]):
        columns = column_data[i].split('\t')
        col1 = columns[colU1]  # .encode('utf-8')
        col2 = columns[colU2]  # .encode('utf-8')
        if col1 == col2:
          continue

        rowNum = i + 1
        col0 = columns[colZ].encode('utf-8')

        # Compute the differences
        # d12 = d.compare(col1, col2)

        diffType = 'Other'
        if nya_pattern.search(col1):
          diffType = 'NYA 1009'
          print('%s NYA PATTERN in %s' % (rowNum, col1.encode('utf-8')))
          pattern_counts[diffType] += 1

        if re.sub(space_pattern, '', col1) == re.sub(space_pattern, '', col2):
          diffType = 'SPACE ONLY'
          pattern_counts[diffType] += 1

        if nya_pattern.sub('\u1025', col1) == col2:
          diffType = 'NYA replacement'
          pattern_counts[diffType] += 1

        # if re.sub(ra_e_pattern, 'u103c\u1031$1', col1) == col2:
        if ra_e_pattern.search(col1):
          diffType = 'Medial Ra - E vowel'

        if re.search(fffd_pattern, col1):
          print('%s FFFD MATCH' % rowNum)
          diffType = 'FFFD'

        #if re.sub(ra_sub_pattern, 'u1030$1\u103C', col1) == col2:
        if ra_sub_pattern.search(col1):
          diffType = 'Medial Ra subscript'

        if digit0_pattern.search(col1) or digit4_pattern.search(col1):
          diffType = 'Digit found C++'

        if digit0_pattern.search(col2) or digit4_pattern.search(col2):
          diffType = 'Digit found in JS'

        pattern_counts[diffType] += 1
        groups.append([rowNum, col0, col1.encode('utf-8'), col2.encode('utf-8'), diffType])

    template_values = {
        'description': 'Compare Burmese conversion C++ vs. Javascript',

        'encodingFonts': ['ZawgyiOne', 'NotoSansMyanmar', 'NotoSansMyanmar'],
        'groups': groups,
        'pattern_counts': pattern_counts,
    }

    path = os.path.join(os.path.dirname(__file__), 'comparecolumns.html')
    self.response.out.write(template.render(path, template_values))

    return


# Main handler setup.
app = webapp2.WSGIApplication([
    ('/comp/text/', compareHandler),
    ('/comp/columns/', compareColumnsHandler),
    ], debug=True)
