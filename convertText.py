#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Text conversion utilities."""

def convertBytestoCharacters(text_in, base):

  print '** text_in = %s' % text_in
  text_out = text_in.decode('utf-8')
  print '!!! text_out = %s' % text_out
  return text_out
  