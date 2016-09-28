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
import convertHandler
import convertText
import detector
import feedback
import fontrules
import detector

import sendmail
import transliterate
import translit_myazedi
import translit_uni_mon  # For UniMon text -> UniCode
import translit_monuni  # For Mon "Unicode" text -> UniCode
import translit_mon  # For Mon text -> UniCode
import translit_knu  # For Karen KNU encoded text -> UniCode
import translit_zawgyi  # import ZAWGYI_UNICODE_TRANSLITERATE, description
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
default_converter = None
myazedi_converter = None
unimon_converter = None
mon_converter = None
knu_converter = None

def SetDefaultTemplate(text):
  if text:
    template_values = {
      'input_text': text,
      'default_zawgyi': text,
      'default_z2008': text,
      'default_unicode': text,
      'default_myazedi': text,
      'default_unimon': text
    }
  else:
    template_values = {
      'input_text': text,
      'default_zawgyi': 'z ဘယ္',
      'default_z2008': 'z2008 ယခင္သိုႛ',
      'default_unicode': 'u လောက်က',
      'default_myazedi': 'm ဆီၾဒင္',
      'default_unimon': default_unimon,
      'default_knu': default_knu,
      
    }
  return template_values

class MainHandler(webapp2.RequestHandler):
  def get(self):
  
    text = self.request.get("text", "")
    template_values = SetDefaultTemplate(text)
      
    path = os.path.join(os.path.dirname(__file__), 'mainmyfonts.html')
    self.response.out.write(template.render(path, template_values))


class MainHandler2(webapp2.RequestHandler):
  def get(self):
  
    text = self.request.get("text", "")
  
    template_values = SetDefaultTemplate(text)
        
    path = os.path.join(os.path.dirname(__file__), 'mainmyfonts2.html')
    self.response.out.write(template.render(path, template_values))

        
class DetectionHandler(webapp2.RequestHandler):
  def get(self):
    text = self.request.get("text", "")
    self.response.headers['Content-Type'] = 'application/json'   
    if (text):  
      # Call detectors and return values.
      isZ = detector.isZawgyi(text);
      isU = detector.isUnicode(text);
      isZShake = detector.isZawgyiShake(text);
      isUShake = detector.isUnicodeShake(text);
      isMyazedi = detector.isMyazedi(text);
      
      obj = { 'input': text,
               'isZ': isZ, 'isU': isU,
               'isZShake': isZShake, 'isUShake': isUShake,
               'isMyazedi': isMyazedi,
               'errmsg': 'OK' }
    else:
      obj = { 'input': text,
              'errmsg': 'Null input' }
    self.response.out.write(json.dumps(obj))

    
class CompareTextHandler(webapp2.RequestHandler):
  def get(self):
  
    text1 = self.request.get("text1", "")
    text2 = self.request.get("text2", "")

    template_values = {
      't1': text1,
      'font1': self.request.get("font1", "notosans"),
      't2': text2,
      'font2': self.request.get("font2", "notosans")
    }
  
    logging.info('CompareTextHandler: %s vs %s' % (text1, text2))
    path = os.path.join(os.path.dirname(__file__), 'compare.html')
    self.response.out.write(template.render(path, template_values))


# Convert text in URL, with JSON return
class ConvertHandler(webapp2.RequestHandler):
  def post(self):
    self.response.headers['Content-Type'] = 'text/plain'   

    print 'ConvertHandler get received.'
    self.response.out.write('ConvertHandler get received.\n')

  def get(self):
    global default_converter
    global myazedi_converter
    global unimon_converter
    global mon_converter
    global knu_converter

    if not default_converter:
      default_converter = transliterate.Transliterate(
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
    
    logging.info('CONVERT %d characters' % len(input))

    if input_type == 'M':
      if not myazedi_converter:
        myazedi_converter = transliterate.Transliterate(
          translit_myazedi.MYAZEDI_UNICODE_TRANSLITERATE,
          translit_myazedi.MYAZEDI_description)
      result = myazedi_converter.transliterate(input, debug)
      msg = 'Myazedi conversion'
    elif input_type == 'Z':
      # Zawgyi
      result = default_converter.transliterate(input)
      msg = 'From Zawgyi'
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
          translit_mon.MON_MONUNI_TRANSLITERATE,
          translit_mon.MON_MONUNI_description)
      result = mon_converter.transliterate(input, debug)
      msg = 'Mon Unicode conversion'    
    elif input_type == "MON":
      if not mon_converter:
        mon_converter = transliterate.Transliterate(
          translit_mon.MON_UNICODE_TRANSLITERATE,
          translit_mon.MON_description)
      result = mon_converter.transliterate(input, debug)
      msg = translit_mon.MON_description
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
      msg = 'Karen conversion'    
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
              'detector_description': default_converter.description,
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


# Shows user interface for converting from Zawgyi & Myazedi 
class ConvertUIHandler(webapp2.RequestHandler):
  # Show feedback form.
  def get(self):
    text = self.request.get("text", "")
    template_values = SetDefaultTemplate(text)
    
    path = os.path.join(os.path.dirname(__file__), 'convert.html')
    self.response.out.write(template.render(path, template_values))

# Shows user interface for converting from Zawgyi, Myazedi, and Mon fonts. 
class Convert2UIHandler(webapp2.RequestHandler):
  # Show feedback form.
  def get(self):
    text = self.request.get("text", "")
    template_values = SetDefaultTemplate(text)
    
    path = os.path.join(os.path.dirname(__file__), 'convert2.html')
    self.response.out.write(template.render(path, template_values))

# Shows user interface for converting from Zawgyi, Myazedi, and Mon fonts. 
class MonHandler(webapp2.RequestHandler):
  # Show feedback form.
  def get(self):
    text = self.request.get("text", "")
    template_values = SetDefaultTemplate(text)
    
    path = os.path.join(os.path.dirname(__file__), 'mon.html')
    self.response.out.write(template.render(path, template_values))

# Shows user interface for converting from Zawgyi, Myazedi, and Mon fonts. 
class KarenHandler(webapp2.RequestHandler):
  # Show feedback form.
  def get(self):
    text = self.request.get("text", "")
    template_values = SetDefaultTemplate(text)
    
    path = os.path.join(os.path.dirname(__file__), 'karen.html')
    self.response.out.write(template.render(path, template_values))

# Shows user interface for Shan fonts and conversions. 
class ShanHandler(webapp2.RequestHandler):
  # Show feedback form.
  def get(self):
    text = self.request.get("text", "")
    template_values = SetDefaultTemplate(text)

    logging.info('SHAN: %s' % text)
    
    path = os.path.join(os.path.dirname(__file__), 'shan.html')
    self.response.out.write(template.render(path, template_values))


# Given 'Z' or 'M', return the rules and description as JSON.
class GetRulesHandler(webapp2.RequestHandler):
  def get(self):
    global default_converter
    global myazedi_converter

    input_type = self.request.get('type', 'Z')
    msg = ''
    errmsg = None
    
    debug = 1
    if input_type == 'M':
      rules = translit_myazedi.MYAZEDI_UNICODE_TRANSLITERATE
      description = translit_myazedi.MYAZEDI_description
    elif input_type == 'Z':
      # Zawgyi
      rules = translit_zawgyi.ZAWGYI_UNICODE_TRANSLITERATE
      description = translit_zawgyi.ZAWGYI_description
    else:
      rules = ''
      description = ''
      errmsg = 'Unknown converter type = %s' % input_type
    
    self.response.headers['Content-Type'] = 'application/json'   
    # Call the converter on this text data.
    obj = { 'input_type': input_type,
            'rules': rules,
            'detector_description': description,
            'errmsg': errmsg
    }
    self.response.out.write(json.dumps(obj))


# Run tests of the transliterators.
class TestTranslitHandler(webapp2.RequestHandler):
  def get(self):
    testKit = translittests.translitRegression()

    listResults = testKit.listTest()

    extraResults = testKit.testExtra()
    paragraphResults = testKit.testParagraphs()
    zeroWidthResults = testKit.testZeroWidthSpace()
 
    self.response.headers['Content-Type'] = 'text/plain'   

    self.response.out.write('listTest results = %s.\n\n' % listResults)
    self.response.out.write('Extra test results = %s.\n\n' % extraResults)
    self.response.out.write('Paragraph results:\n')
    for result in paragraphResults:
      self.response.out.write('  %s\n' % result)

    self.response.out.write('\n')
    for result in zeroWidthResults:
      self.response.out.write('%s\n' % result)    
 
  
# Trial segmentation
class SegmentHandler(webapp2.RequestHandler):

  def get(self):
    text = self.request.get("text", "")

    template_values = {
      't1': text,
    }
    path = os.path.join(os.path.dirname(__file__), 'segment.html')
    self.response.out.write(template.render(path, template_values))


# Returns converted characters from input bytes, hex by default.
class convertBtoCHandler(webapp2.RequestHandler):
  def get(self):
  
    hex_text = self.request.get("text", "")
    input_type = self.request.get("input_type", "16")  # Could also be octal (8).
    
    print 'hext_text = %s' % hex_text.decode('utf-8')
    
    outChars = convertText.convertBytestoCharacters(hex_text, input_type)
    print '%%%%%%%%%% outChars = %s' % outChars

    self.response.headers['Content-Type'] = 'application/json'   
     
    # Call the converter on this text data.
    obj = { 'input': hex_text,
            'input_type': input_type,
            'converted': outChars,
            'errmsg': None }

    self.response.out.write(json.dumps(obj))    

# Show the ranges for the languages
class RangeHandler(webapp2.RequestHandler):
  def get(self):
    for lang in charRanges.codeList:
      lang.expand()
    template_values = {'ranges': charRanges.codeList,
    }
    path = os.path.join(os.path.dirname(__file__), 'ranges.html')
    self.response.out.write(template.render(path, template_values))


# test for madlib handling
class madlibHandler(webapp2.RequestHandler):
  def get(self):
    template_values = {}
    path = os.path.join(os.path.dirname(__file__), 'madlib.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):
    template_values = {arg: self.request.get_all(arg)[0] for arg in self.request.arguments()}
    logging.info("template_values: %s\n" % (template_values))

    path = os.path.join(os.path.dirname(__file__), 'madlibresults.html')
    self.response.out.write(template.render(path, template_values))


# Return help for commands
class HelpHandler(webapp2.RequestHandler):
  def get(self):
  
    text = self.request.get("text", "")
  
    helpText = """
    ('/', MainHandler),
    ('/t2', MainHandler2),
    ('/feedback', FeedbackHandler),
    ('/detect/', DetectionHandler),
    ('/convertui/', ConvertUIHandler),
    ('/burmese/', ConvertUIHandler),
    ('/zawgyi/', ConvertUIHandler),
    ('/convert2/', Convert2UIHandler),
    ('/convert/', ConvertHandler),
    ('/getrules/', GetRulesHandler),
    ('/compare/', CompareTextHandler),
    ('/testtransliteration/', TestTranslitHandler),
    ('/segment/', SegmentHandler),
    ('/convertBtoC/', convertBtoCHandler),
    ('/convert2ui/', convertBtoCHandler),
    ('/mon/', MmonHandler),
    ('/karen/', KarenHandler),
    ('/shan/', ShanHandler),
    ('/ranges/', RangeHandler),
    ('/detect/', markovDetect.DetectHandler),
    ('/detectResult/', markovDetect.DetectResultHandler),
    ('/ComputeModel/', detector.ComputeModel),
	('/ShowAllModels/ ', detector.ShowAllModels),
    ('/submiterror/', SubmitErrorHandler),
    ('/help/', HelpHandler)
    """

    self.response.headers['Content-Type'] = 'text/plain'   
    self.response.out.write('commands:%s' % helpText)
   

# Return help for commands
def intWithCommas(x):
    #if type(x) not in [type(0), type(0L)]:
    #    raise TypeError("Parameter must be an integer.")
    if x < 0:
        return '-' + intWithCommas(-x)
    result = ''
    while x >= 1000:
        x, r = divmod(x, 1000)
        result = ",%03d%s" % (r, result)
    return "%d%s" % (x, result)
    
  
# Main handler setup.
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/t2/', MainHandler2),
    ('/convertui/', ConvertUIHandler),
    ('/convert2/', Convert2UIHandler),
    ('/convert/', convertHandler.ConvertHandler),  # Handles backend conversions.
    ('/getrules/', GetRulesHandler),
    ('/compare/', CompareTextHandler),
    ('/testtransliteration/', TestTranslitHandler),
    ('/segment/', SegmentHandler),
    ('/convertBtoC/', convertBtoCHandler),
    ('/zawgyi/', ConvertUIHandler),
    ('/burmese/', ConvertUIHandler),
    ('/karen/', KarenHandler),
    ('/mon/', MonHandler),
    ('/shan/', ShanHandler),
    ('/fontrules/', fontrules.FontRulesHandler),
    ('/help/', HelpHandler),

    ('/feedback/', feedback.FeedbackHandler),
    ('/entererror/', feedback.SubmitErrorHandler),
    ('/store_error_sample/', feedback.StoreErrorHandler),
    ('/getfeedback/', feedback.GetFeedbackHandler),
    
    ('/detect/', detector.DetectHandler),
    ('/detectResult/', detector.DetectResultHandler),
    ('/ComputeModel/', detector.ComputeModel),
	('/ShowAllModels/', detector.ShowAllModels),
	('/ShowModelDetail/', detector.ShowModelDetail), 
    ('/ranges/', RangeHandler),
    
    ('/madlib/', madlibHandler)

  ], debug=True)
