#!/usr/bin/env python
# -*- coding: utf-8 -*-

import transliterate
import translit_unicode2zawgyi

import sys


uz_converter = None


def runTests():
  testdata = translit_unicode2zawgyi.TestData()

  debug = True
  index = 0
  for expected, input in testdata:
    print
    print '-'*60
    print 'Test %2d: %s --> %s' % (index, input.encode('utf-8'),
                                   expected.encode('utf-8'))
    result = uz_converter.transliterate(input, debug)
    if result == expected:
      print 'PASS %s: in=%s, result=%s, expected = %s' % (index, input.encode('utf-8'),
                                                                result.encode('utf-8'),
                                                                expected.encode('utf-8'))
    else:
      print 'FAIL: %s: in=%s, result=%s, expected = %s' % (index, input.encode('utf-8'),
                                                                result.encode('utf-8'),
                                                                expected.encode('utf-8'))
      print '  result:   %s\n  expected: %s' % (
          transliterate.uStringToHex(result),
          transliterate.uStringToHex(expected)
      )

    index += 1


def main(args):
  global uz_converter
  uz_converter = transliterate.Transliterate(
      translit_unicode2zawgyi.UNICODE_ZAWGYI_TRANSLITERATE,
      translit_unicode2zawgyi.UZ_description)

  print 'RULES FOR %s' % translit_unicode2zawgyi.UZ_description

  uz_converter.summary(show_rules=True)

  runTests()


if __name__ == "__main__":
    print 'ARGS = %s' % sys.argv
    sys.exit(main(sys.argv))
