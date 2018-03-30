#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import os
import urllib
import webapp2

from google.appengine.ext.webapp import template

# For internationalization
from django.utils.translation import ugettext as _
from django.conf import settings

import charRanges
import convertText
import detector
import feedback

import sendmail
import transliterate
import translit_myazedi
import translit_uni_mon  # For UniMon text -> UniCode
import translit_monuni  # For Mon "Unicode" text -> UniCode
import translit_mon  # For Mon text -> UniCode
import translit_knu  # For Karen KNU encoded text -> UniCode
import translit_sawcfcr000  # Karen Saw font encoded -> UniCode
import translit_zwekabin  # For Karen Zwekabin encoded text -> UniCode

import translit_zawgyi  # import ZAWGYI_UNICODE_TRANSLITERATE, description

import translit_unicode2zawgyi

import translittests

# Data store
import testString

# Globals
default_zawgyi = 'z ဘယ္'
default_z2008= 'z2008 ယခင္သိုႛ'
default_unicode = 'u လောက်က'
default_myazedi = 'm ဆီၾဒင္'
default_unimon = 'ကၝကၞကၟ'
default_knu = 'w> *h> vdm bSD vdm td. xD. vX bD u x. xH w rX. w> wdm usJR'
default_saw = 'e>Iog\'D; wIwDwIvd: vUtwI\'d;e>I tcGJ;t<PwzOe>O'
zawgyi_converter = None
myazedi_converter = None
unimon_converter = None
mon_converter = None
mon_uni_converter = None
knu_converter = None
saw_converter = None
zwekabin_converter = None

uz_converter = None


# Convert text in URL, with JSON return
class ConvertHandler(webapp2.RequestHandler):
  def post(self):
    self.response.headers['Content-Type'] = 'text/plain'

    print 'ConvertHandler get received.'
    self.response.out.write('ConvertHandler post received.\n')

  def get(self):
    global knu_converter
    global mon_converter
    global mon_uni_converter
    global myazedi_converter
    global saw_converter
    global unimon_converter
    global zawgyi_converter
    global zwekabin_converter
    global uz_converter

    if not zawgyi_converter:
      zawgyi_converter = transliterate.Transliterate(
        translit_zawgyi.ZAWGYI_UNICODE_TRANSLITERATE,
        translit_zawgyi.ZAWGYI_description)

    text = unicode(self.request.get('text'))
    logging.info('text         = %s' % text)
    input_type = self.request.get('type', 'Z')
    strip_spaces = self.request.get('strip_spaces', None)
    debug = self.request.get('debug', None)

    input = urllib.unquote(text) #   .decode('utf-8')
    logging.info('decoded text = %s' % text)

    noreturn = self.request.get('noreturn', None)
    msg = ''

    logging.info('Type = %s, CONVERT %d characters' %
        (input_type, len(input)))

    if input_type == 'M':
      if not myazedi_converter:
        myazedi_converter = transliterate.Transliterate(
          translit_myazedi.MYAZEDI_UNICODE_TRANSLITERATE,
          translit_myazedi.MYAZEDI_description)
      result = myazedi_converter.transliterate(input, debug)
      msg = translit_myazedi.MYAZEDI_description
    elif input_type == 'Z':
      if not zawgyi_converter:
        zawgyi_converter = transliterate.Transliterate(
          translit_zawgyi.ZAWGYI_UNICODE_TRANSLITERATE,
          translit_zawgyi.ZAWGYI_description)      # Zawgyi
      result = zawgyi_converter.transliterate(input)
      msg = translit_zawgyi.ZAWGYI_description

        # Mon language conversions
    elif input_type == "UNIMON":  # Also Mon 2010 (mostly)
      if not unimon_converter:
        unimon_converter = transliterate.Transliterate(
          translit_uni_mon.UNIMON_UNICODE_TRANSLITERATE,
          translit_uni_mon.UNIMON_description)
      result = unimon_converter.transliterate(input, debug)
      msg = translit_uni_mon.UNIMON_description
    elif input_type == "MONUNI":
      if not mon_uni_converter:
        mon_uni_converter = transliterate.Transliterate(
          translit_monuni.MON_MONUNI_TRANSLITERATE,
          translit_monuni.MON_MONUNI_description)
      result = mon_uni_converter.transliterate(input, debug)
      msg = translit_monuni.MON_MONUNI_description
    elif input_type == "MON":
      if not mon_converter:
        mon_converter = transliterate.Transliterate(
          translit_mon.MON_UNICODE_TRANSLITERATE,
          translit_mon.MON_description)
      result = mon_converter.transliterate(input, debug)
      msg = translit_mon.MON_description

        # Karen font conversions
    elif input_type == "KNU":
      if not knu_converter:
        knu_converter = transliterate.Transliterate(
          translit_knu.KNU_UNICODE_TRANSLITERATE,
          translit_knu.KNU_description)
      # Preprocess with string substitution
      # logging.info('***knu input = %s' % input);
      for rep in translit_knu.KNU_substitutions:
        text = input.replace(rep[0], rep[1])
        input = text

      logging.info('***knu strip_spaces = %s' % strip_spaces);
      if strip_spaces:
         input = input.replace(' ', '')

      result = knu_converter.transliterate(input, debug)
      # logging.info('***knu result = %s' % result);
      msg = translit_knu.KNU_description
    elif input_type == 'SAW':
      if not saw_converter:
        saw_converter = transliterate.Transliterate(
          translit_sawcfcr000.UNICODE_TRANSLITERATE,
          translit_sawcfcr000.description)
      # Preprocess with string substitution
      logging.info('***SAW input = %s' % input);
      for rep in translit_sawcfcr000.substitutions:
        text = input.replace(rep[0], rep[1])
        input = text

      logging.info('***saw strip_spaces = %s' % strip_spaces);
      if strip_spaces:
         input = input.replace(' ', '')

      result = saw_converter.transliterate(input, debug)
      logging.info('***saw result = %s' % result);
      msg = 'Karen SAW conversion'


    elif input_type == 'U':
      # Unicode to (ahem) Z
      if not uz_converter:
        uz_converter = transliterate.Transliterate(
          translit_unicode2zawgyi.UNICODE_ZAWGYI_TRANSLITERATE,
          translit_unicode2zawgyi.UZ_description)
      result = uz_converter.transliterate(input)
      msg = translit_unicode2zawgyi.UZ_description

    else:
      msg = 'Unknown encoding = %s!' % input_type
      result = 'No conversion attempted.'

    self.response.headers['Content-Type'] = 'application/json'
    if input:
      if noreturn:
        returntext = ''
      else:
         returntext = text

      logging.info('RESULT has %d characters' % len(result))

      # Call the converter on this text data.
      obj = { 'input': returntext,
              'input_type': input_type,
              'msg': msg,
              'converted': result,
              'detector_description': zawgyi_converter.description,
              'noreturn': noreturn,
              'inputSize': len(input),
              'resultSize': len(result),
              'errmsg': None }
    else:
      obj = { 'input': text,
              'input_type': input_type,
              'msg': msg,
              'noreturn': noreturn,
              'errmsg': 'Null input' }
    self.response.out.write(json.dumps(obj))
