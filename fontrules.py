#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import os
import urllib
import webapp2

from google.appengine.ext.webapp import template

import transliterate
import translit_zawgyi
import translit_myazedi
import translit_uni_mon  # For UniMon text -> UniCode
import translit_monuni  # For Mon "Unicode" text -> UniCode
import translit_mon  # For Mon text -> UniCode
import translit_knu  # For Karen KNU encoded text -> UniCode
import translit_zwekabin  # For Karen Zwekabin encoded text -> UniCode
import translit_wwinBurma
import translit_mon2012

class langFontInfo():
  # Information about languages
  
  def __init__(self, name):
    self.name = name
    self.fontlist = []

  def addFont(self, fontinfo):
    self.fontlist.append(fontinfo)

class fontInfo():

  def __init__(self, name, rules=None, transform=None, detect=None, notes=None):
    self.name = name
    self.rules = rules
    self.transform = transform
    self.detect = detect
    self.notes = notes

# Convert text in URL, with JSON return
class FontRulesHandler(webapp2.RequestHandler):
  def post(self):
    self.response.headers['Content-Type'] = 'text/plain'   

    print 'ConvertHandler get received.'
    self.response.out.write('ConvertHandler post received.\n')

  def get(self):
  
    burmeseLang = langFontInfo('Burmese')
    zawgyiFont = fontInfo('Zawgyi',
                           rules = translit_zawgyi.TRANS_LIT_RULES,
                           notes = translit_zawgyi.Description)  # Need detector and noes
    burmeseLang.addFont(zawgyiFont)
    
    langlist = [burmeseLang]
    template_values = {
      'langlist': langlist,

    }
    path = os.path.join(os.path.dirname(__file__), 'fontrules.html')
    self.response.out.write(template.render(path, template_values))


encoding_font_list = [
    {
        'font_path':'/fonts/ZawgyiOne.ttf',
        'font_name':'Zawgyi One',
        'display_name': 'Zawgyi One',
    },
#    {
#        'font_path':'/fonts/ZawgyiOne2008.ttf',
#        'font_name':'Zawgyi One 2008',
#        'display_name': 'Zawgyi One 2008',
#    },
#    {
#        'font_path':'/fonts/MyaZedi06.ttf',
#        'font_name':'Myazedi',
#        'display_name': 'MyaZedi06',
#    },
]

unicode_font_list = [
  { 'family': 'NotoSansMyanmar',
    'longName': 'Noto Sans Myanmar',
    'source': '/fonts/NotoSansMyanmar-Regular.ttf',
  },
  { 'family': 'Padauk',
    'longName': 'Padauk',
    'source': '/fonts/Padauk.ttf',
  },
  { 'family': 'MM3',
    'longName': 'Myanyar3',
    'source': '/fonts/mm3.ttf',
  },
]

# Show characters in Unicode and font encodings
class ShowFonts(webapp2.RequestHandler):

  def get(self):
    # Hex codes for characters astride the spaces
    min_code = self.request.get('min', '1000')
    max_code = self.request.get('max', '109f')

    code_before = self.request.get('before', '1000')
    code_before = self.request.get('before', '1000')
    code_after = self.request.get('after', '1002')
    second_space_code = self.request.get('second_space', '200b')

    template_values = {
        'encoding_list': encoding_font_list,
        'unicode_list': unicode_font_list,
        'min_code': int(min_code, 16),
        'max_code': int(max_code, 16),
        'code_before': code_before,
        'code_after': code_after,
        'second_space_code': second_space_code,
        'language': 'Myanmar (Burmese)',
    }

    path = os.path.join(os.path.dirname(__file__), 'fontsView.html')
    self.response.out.write(template.render(path, template_values))
