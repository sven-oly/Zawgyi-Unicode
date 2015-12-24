#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import os
import webapp2

from google.appengine.ext.webapp import template

import convertText
import detector
import sendmail
import transliterate
import translit_myazedi
import translit_zawgyi  # import ZAWGYI_UNICODE_TRANSLITERATE, description
import translittests


# Globals
default_zawgyi = 'z ဘယ္'
default_z2008= 'z2008 ယခင္သိုႛ'
default_unicode = 'u လောက်က'
default_myazedi = 'm ဆီၾဒင္'

default_converter = None
myazedi_converter = None


class MainHandler(webapp2.RequestHandler):
  def get(self):
  
    text = self.request.get("text", "")
  
    if text:
      template_values = {
        'input_text': text,
        'default_zawgyi': text,
        'default_z2008': text,
        'default_unicode': text,
        'default_myazedi': text
      }
    else:
        template_values = {
        'input_text': text,
        'default_zawgyi': 'z ဘယ္',
        'default_z2008': 'z2008 ယခင္သိုႛ',
        'default_unicode': 'u လောက်က',
        'default_myazedi': 'm ဆီၾဒင္'
      }      
    path = os.path.join(os.path.dirname(__file__), 'mainmyfonts.html')
    self.response.out.write(template.render(path, template_values))


class MainHandler2(webapp2.RequestHandler):
  def get(self):
  
    text = self.request.get("text", "")
  
    if text:
      template_values = {
        'input_text': text,
        'default_zawgyi': text,
        'default_z2008': text,
        'default_unicode': text,
        'default_myazedi': text
      }
    else:
        template_values = {
        'input_text': text,
        'default_zawgyi': 'z ဘယ္',
        'default_z2008': 'z2008 ယခင္သိုႛ',
        'default_unicode': 'u လောက်က',
        'default_myazedi': 'm ဆီၾဒင္'
      }      
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
    
    if not default_converter:
      default_converter = transliterate.Transliterate(
        translit_zawgyi.ZAWGYI_UNICODE_TRANSLITERATE,
        translit_zawgyi.ZAWGYI_description)
    
    text = unicode(self.request.get('text')) # .encode('utf-8')
    input_type = self.request.get('type', 'Z')
    debug = self.request.get('debug', None)

    noreturn = self.request.get('noreturn', None)
    msg = ''
    
    
    if input_type == 'M':
      if not myazedi_converter:
        myazedi_converter = transliterate.Transliterate(
          translit_myazedi.MYAZEDI_UNICODE_TRANSLITERATE,
          translit_myazedi.MYAZEDI_description)
      result = myazedi_converter.transliterate(text, debug)
      msg = 'Myazedi conversion'
    elif input_type == 'Z':
      # Zawgyi
      result = default_converter.transliterate(text)
      msg = 'From Zawgyi'
    else:
      msg = 'Unknown encoding!'
      result = 'No conversion attempted.'
    
    self.response.headers['Content-Type'] = 'application/json'   
    if text:
      if noreturn:
        returntext = ''
      else:
         returntext = text
     
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


# Shows user interface for converting from Zawgyi to 
class ConvertUIHandler(webapp2.RequestHandler):
  # Show feedback form.
  def get(self):
    text = self.request.get("text", "")
    template_values = {
      'msg': 'No text'
     }
   
    if text:
      template_values = {
        'input_text': text,
        'default_zawgyi': text,
        'default_myazedi': text
      }
  
    path = os.path.join(os.path.dirname(__file__), 'convert.html')
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
    ('/convert/', ConvertHandler),
    ('/getrules/', GetRulesHandler),
    ('/compare/', CompareTextHandler),
    ('/testtransliteration/', TestTranslitHandler),
    ('/segment/', SegmentHandler),
    ('/convertBtoC/', convertBtoCHandler),
    ('/help/', HelpHandler)
    """

    self.response.headers['Content-Type'] = 'text/plain'   
    self.response.out.write('commands:%s' % helpText)
   



# Main handler setup.
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/t2/', MainHandler2),
    ('/feedback', FeedbackHandler),
    ('/detect/', DetectionHandler),
    ('/convertui/', ConvertUIHandler),
    ('/convert/', ConvertHandler),
    ('/getrules/', GetRulesHandler),
    ('/compare/', CompareTextHandler),
    ('/testtransliteration/', TestTranslitHandler),
    ('/segment/', SegmentHandler),
    ('/convertBtoC/', convertBtoCHandler),
    ('/help/', HelpHandler),
    ('/madlib/', madlibHandler)

  ], debug=True)
