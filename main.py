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

import chrNumerals
import convertText
import detector
import sendmail
import transliterate
import translit_myazedi
import translit_uni_mon  # For UniMon text -> UniCode
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
      't2': text2
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
    
    text = unicode(self.request.get('text')) # .encode('utf-8')
    input_type = self.request.get('type', 'Z')
    debug = self.request.get('debug', None)
    
    input = urllib.unquote(text) #   .decode('utf-8')

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
    elif input_type == "UM":
      if not unimon_converter:
        unimon_converter = transliterate.Transliterate(
          translit_uni_mon.UNIMON_UNICODE_TRANSLITERATE,
          translit_uni_mon.UNIMON_description)
      result = unimon_converter.transliterate(input, debug)
      msg = 'UniMon conversion'    
    elif input_type == "MON":
      if not mon_converter:
        mon_converter = transliterate.Transliterate(
          translit_mon.MON_UNICODE_TRANSLITERATE,
          translit_mon.MON_description)
      result = mon_converter.transliterate(input, debug)
      msg = 'Mon conversion'    
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
      result = knu_converter.transliterate(input, debug)
      # logging.info('***knu result = %s' % result);
      msg = 'Karen conversion'    
    else:
      msg = 'Unknown encoding!'
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

# Shows user interface for Shan fonts and conversions. 
class SubmitErrorHandler(webapp2.RequestHandler):
  # Show feedback form.
  def get(self):
    text = self.request.get("text", "")
    template_values = SetDefaultTemplate(text)

    logging.info('Submit error: %s' % text)
    
    path = os.path.join(os.path.dirname(__file__), 'submitError.html')
    self.response.out.write(template.render(path, template_values))


class StoreErrorHandle(webapp2.RequestHandler):
  # Show feedback form.
  def get(self):
    text = self.request.get("text", "")
    template_values = SetDefaultTemplate(text)

    logging.info('StoreErrorHandle error: %s' % text)
    
    # TODO: Create a new error entry and store it.
    
    path = os.path.join(os.path.dirname(__file__), 'storedError.html')
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
 
  
class FeedbackHandler(webapp2.RequestHandler):
  # Show feedback form.
  def get(self):
  
    template_values = {
    
    }
    path = os.path.join(os.path.dirname(__file__), 'feedback.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):
    # Handle response to feedback data.  

    sender_name = self.request.get('name')
    description = self.request.get('description')
    sender_email = self.request.get('email')

    logging.info('Sender: %s (%s)\n' % (sender_name, sender_email))
    logging.info("Description received = '%s'\n" % description)

    email_body = ('sender: %s (%s)\n \nDescription: %s\n' %
                   (sender_name, sender_email, description))

    result = sendmail.send_mail('smtpauth.earthlink.net',
         None, 'cwcornelius@gmail.com','cwcornelius@gmail.com',
         'Feedback', email_body, False)
          
    template_values = {
      'result': result
    }
    logging.info("EMail result: %s\n" % (result))

    path = os.path.join(os.path.dirname(__file__), 'sendfeedback.html')
    self.response.out.write(template.render(path, template_values))


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
    ('/submiterror/', SubmitErrorHandler),
    ('/help/', HelpHandler)
    """

    self.response.headers['Content-Type'] = 'text/plain'   
    self.response.out.write('commands:%s' % helpText)
   

# Return help for commands
class chrNumeralsHandler(webapp2.RequestHandler):
  def get(self):
    text = self.request.get('number', '')
    debug = self.request.get('debug', 'off')
    logging.info('input number is %s' % text)

    if text == '' or text == None:
      numeralList = []
    else:
      numeralList = chrNumerals.digitalToSequoah(int(text))

    messageTrans = 'no translation'
    # TODO: Activate this. messageTrans = _("testmsg")
    
    template_values = {
        'number': text,
        'numeralList': numeralList,
        'debug_state': debug,
        'testMsg': messageTrans
	}
	
    
    path = os.path.join(os.path.dirname(__file__), 'chrNumerals.html')
    self.response.out.write(template.render(path, template_values))

# Handles decimal conversion from front end.
class chrDecimalNumeralsHandler(webapp2.RequestHandler):
  def get(self):
    text = self.request.get('number', '')
    debug = self.request.get('debug', 'off')
    logging.info('input number is %s' % text)
    if text == '' or text == None:
      numeralList = []
    else:
      text = text.replace(',', '')
      lists = numeralList = chrNumerals.digitalToSequoah(int(text))
      numeralList = lists[1]
      stringList = lists[0]
    logging.info('digitalToSequoah =  %s' % numeralList)
   
    template_values = {
        'number': text, 'numeralList': numeralList, 
        'stringList': stringList,
        'debug_state': debug
    }
    self.response.out.write(json.dumps(template_values))

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
    
# Handles CHR numerals to decimal conversion from front end.
class chrToDecimalHandler(webapp2.RequestHandler):
  def get(self):
    debug = self.request.get('debug', 'off')
    codes = self.request.get('chrCodes', '')
    logging.info('input number is %s' % codes)
    if codes == '' or codes == None:
      codes = []
      decimal = -1
      formattedValue = 'PROBLEMS'  
    else:
      decimal = chrNumerals.processCodes(codes)
      formattedValue = intWithCommas(decimal)
      logging.info('FORMATTED = %s' % formattedValue)
    template_values = {
        'decimal': decimal,
        'formatted': formattedValue,
     	'codes': codes,
        'debug_state': debug
	}
    self.response.out.write(json.dumps(template_values))

# Calls tests, shows results.
class sequoyahTestHandler(webapp2.RequestHandler):
  def get(self):
    test1Results = chrNumerals.testChrToDec()  
    test2Results = chrNumerals.testDecToChr()
    template_values = {
      'CHR to decimal': test1Results,
      'Decimal to CHR': test2Results,
      'debug_state': 'on'
	}
    self.response.out.write(json.dumps(template_values))
          
# Main handler setup.
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/t2/', MainHandler2),
    ('/feedback', FeedbackHandler),
    ('/detect/', DetectionHandler),
    ('/convertui/', ConvertUIHandler),
    ('/convert2/', Convert2UIHandler),
    ('/convert/', ConvertHandler),
    ('/getrules/', GetRulesHandler),
    ('/compare/', CompareTextHandler),
    ('/testtransliteration/', TestTranslitHandler),
    ('/segment/', SegmentHandler),
    ('/convertBtoC/', convertBtoCHandler),
    ('/zawgyi/', ConvertUIHandler),
    ('/karen/', KarenHandler),
    ('/mon/', MonHandler),
    ('/shan/', ShanHandler),
    ('/help/', HelpHandler),
    ('/entererror/', SubmitErrorHandler),
    ('store_error_sample', StoreErrorHandle),
    
    ('/madlib/', madlibHandler),
    ('/sequoyahsNumerals/', chrNumeralsHandler),
    ('/setDecimalNumerals/', chrDecimalNumeralsHandler),
    ('/chrToDecimal/', chrToDecimalHandler),
    ('/sequoyahTest/', sequoyahTestHandler)


  ], debug=True)
