#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import os
import urllib
import webapp2

from google.appengine.ext.webapp import template


class ZDecodeHandler(webapp2.RequestHandler):
  def get(self):

    text = self.request.get("text", "")

    template_values = {

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
