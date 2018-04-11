#!/usr/bin/env python
# -*- coding: utf-8 -*-

import transliterate
import translit_unicode2zawgyi
import translit_zawgyi

import sys


# Compiles the transliteration rules into Javascript code, using
# regular expressions.

transObj = None

class compileTranslitRules():

  def __init__(self, translit=None):
    # Initialize member values
    self.translit = translit
    self.js_output = ''

  def compile(self):
    if not self.translit:
      return None

    # For each phase, for each rule
    self.js_output = []
    phases = self.translit.getPhaseList()

    for phase in phases:
      phase_rules = []
      for rule in phase.RuleList:
        phase_rules.append((rule.pattern, rule.subst))

      self.js_output.append(phase_rules)

      # Lots more to do here.

  def printJS(self):
    print 'Javascript output'
    print self.js_output


def compileTranslit():

  debug = True
  index = 0
  passing = []
  failing = []

  # TODO: Fill in

  print 'FAIL = %s' % failing
  print 'PASS = %s' % passing


def main(args):
  global uz_converter
  z2u = transliterate.Transliterate(
    translit_zawgyi.TRANS_LIT_RULES,
    translit_zawgyi.Description)

  print 'RULES FOR %s' % z2u.description
  compiler = compileTranslitRules(z2u)
  compiler.compile()
  compiler.printJS()


if __name__ == "__main__":
    print 'ARGS = %s' % sys.argv
    sys.exit(main(sys.argv))
