#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import os
import urllib
import webapp2

from google.appengine.ext.webapp import template

font_encodings = [
    'Zawgyi2009', 'Zawgyi2008', 'Zawgyi2007']

unicode_fonts = [
    'NotoSans',
    'MonAnonta', 'MM3',
    'Padauk', 'PangLong',
]

zdecode_fonts = [
    { 'display': 'ZDecode 6',
      'family': 'ZDecode6'
    },
    { 'display': 'ZDecode 6 Bold',
      'family': 'ZDecode6Bold'
    },
    { 'display': 'ZDecode Older',
      'family': 'ZDecode'
      }
]


class ZDecodeHandler(webapp2.RequestHandler):
  def get(self):

    text = self.request.get("text", "")

    template_values = {
        'font_encodings': font_encodings,
        'unicode_font_list': unicode_fonts,
        'zdecode_font_list': zdecode_fonts,
    }

    path = os.path.join(os.path.dirname(__file__), 'zdecode.html')
    self.response.out.write(template.render(path, template_values))


# Main handler setup.
app = webapp2.WSGIApplication([
    ('/zdecode/', ZDecodeHandler),
  ],
  debug=True,
  config = {'info': None}
)
