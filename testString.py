#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import ndb

class TestString(ndb.Model):
    """A main model for representing an individual user feedback entry."""
    inputString = ndb.StringProperty(indexed=False)
    convertedString = ndb.StringProperty(indexed=False)
    comment = ndb.StringProperty(indexed=False)
    detectedEncoding = ndb.StringProperty(indexed=False)
    detectedLanguage = ndb.StringProperty(indexed=False)
    dateSubmitted = ndb.DateTimeProperty(auto_now_add=True)
    result = ndb.StringProperty(indexed=False)