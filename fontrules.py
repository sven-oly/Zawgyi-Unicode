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