#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Handle feedback storing the data from user comments.

import json
import logging
import os
import urllib
import webapp2

from google.appengine.ext.webapp import template

from google.appengine.ext import ndb

import sendmail

class ErrorReport(ndb.Model):
    """A main model for representing an individual ErrorReport entry."""
    submitterName = ndb.StringProperty(indexed=False)
    submitterMail = ndb.StringProperty(indexed=False)
    language = ndb.StringProperty(indexed=False)
    encoding = ndb.StringProperty(indexed=False)
    font = ndb.StringProperty(indexed=False)
    sampleText = ndb.StringProperty(indexed=False)
    comment = ndb.StringProperty(indexed=False)
    datetime = ndb.DateTimeProperty(auto_now_add=True)

class FeedbackHandler(webapp2.RequestHandler):
  # Show feedback form.
  def get(self):
  
    template_values = {
      'language': self.request.get('language', 'burmese'),
      'sampleText': self.request.get('sampleText', 'SAMPLE TEXT'),
      'font': self.request.get('font', 'notosans'),
    }
    logging.info('Feedback input = %s %s %s' % (template_values['language'],
    	template_values['font'], template_values['sampleText']))

    path = os.path.join(os.path.dirname(__file__), 'feedback.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):
    # Handle response to feedback data.  

    sender_name = self.request.get('name')
    description = self.request.get('description')
    sender_email = self.request.get('email')
    lang = self.request.get('language', 'burmese')
    encoding = self.request.get('encoding', 'DEFAULT ENCODING')
    font = self.request.get('font', 'notosans')
    comment = self.request.get('commment', 'DEFAULT COMMENT')
    sampleText = self.request.get('sampleText', 'SAMPLE TEXT')

    logging.info('Feedback input = %s %s %s' % (lang, font, sampleText))

    # Create the ErrorReport
    newReport = ErrorReport()
    newReport.submitterName = sender_name
    newReport.submitterMail = sender_email
    newReport.encoding = encoding
    newReport.language = lang
    newReport.comment = comment
    newReport.font = font
    newReport.sampleText = sampleText
    
    # Write to datastore.
    newReport.put()
    
    logging.info('Sender: %s (%s)\n' % (sender_name, sender_email))
    logging.info("Description received = '%s'\n" % description)

    email_body = ('sender: %s (%s)\n \nDescription: %s\n' %
                   (sender_name, sender_email, description))

    result = sendmail.send_mail('smtpauth.earthlink.net',
         None, 'cwcornelius@gmail.com','cwcornelius@gmail.com',
         'Feedback', email_body, False)
      
    template_values = {
      'language': lang,
      'sampleText': sampleText,
      'font': font,
      'encoding': encoding,
      'result': result
    }
    logging.info("EMail result: %s\n" % (result))

    path = os.path.join(os.path.dirname(__file__), 'sendfeedback.html')
    self.response.out.write(template.render(path, template_values))


class SubmitErrorHandler(webapp2.RequestHandler):
  # Show feedback form.
  def get(self):
    text = self.request.get("text", "")
    template_values = {
      'input': self.request.get("text", ""),
      'converted': self.request.get("converted", ""),
      'type': self.request.get("type", "")
    }

    logging.info('Submit error: %s' % text)
    
    path = os.path.join(os.path.dirname(__file__), 'submitError.html')
    self.response.out.write(template.render(path, template_values))


class StoreErrorHandler(webapp2.RequestHandler):
  # Show feedback form.
  def get(self):
    text = self.request.get("text", "")
    template_values = SetDefaultTemplate(text)

    logging.info('StoreErrorHandle error: %s' % text)
    
    # TODO: Create a new error entry and store it.
    
    path = os.path.join(os.path.dirname(__file__), 'storedError.html')
    self.response.out.write(template.render(path, template_values))


class GetFeedbackHandler(webapp2.RequestHandler):
  # Get the data in the data store.
  def get(self):
    lang = self.request.get('lang', '')
    encoding = self.request.get('encoding', '')
    
    results = ErrorReport.query().order(-ErrorReport.datetime)
    numResults = 0
    for r in results:
      numResults += 1 
    logging.info('numResults: %d\n' % (numResults))
    template_values = {
      'lang': lang,
      'encoding': encoding,
      'numResults': numResults,
      'results': results
    }

    logging.info('feedbackResults: %s' % results)
    
    path = os.path.join(os.path.dirname(__file__), 'feedbackResults.html')
    self.response.out.write(template.render(path, template_values))