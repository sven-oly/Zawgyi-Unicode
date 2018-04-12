#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Tests conversion from Zawgyi to Unicode.
import transliterate
import translit_zawgyi

import sys


zu_converter = None


def runTests():
  testdata = translit_zawgyi.TestData()

  debug = True
  index = 0
  passing = []
  failing = []
  for test_num, input, expected, comment in testdata:
    print
    print '-'*60
    try:
      print 'Test %2d "%s": %s --> %s' % (test_num, comment,
                                          input.encode('utf-8'),
                                          expected.encode('utf-8'))
    except:
      print 'TEST CANNOT PRINT %s' % index

    result = zu_converter.transliterate(input, debug)
    if result == expected:
      print 'PASS %s: in=%s, result=%s, expected = %s' % (index, input.encode('utf-8'),
                                                                result.encode('utf-8'),
                                                                expected.encode('utf-8'))
      passing.append(index)
    else:
      print 'FAIL: %s: in=%s, result=%s, expected = %s' % (index, input.encode('utf-8'),
                                                                result.encode('utf-8'),
                                                                expected.encode('utf-8'))
      print '  result:   %s\n  expected: %s' % (
          transliterate.uStringToHex(result),
          transliterate.uStringToHex(expected)
      )
      failing.append(index)

    index += 1

  print 'FAIL = %s' % failing
  print 'PASS = %s' % passing


def main(args):
  global zu_converter
  zu_converter = transliterate.Transliterate(
      translit_zawgyi.TRANS_LIT_RULES,
      translit_zawgyi.Description)

  print 'RULES FOR %s' % translit_zawgyi.Description

  zu_converter.summary(show_rules=True)

  runTests()


if __name__ == "__main__":
    print 'ARGS = %s' % sys.argv
    sys.exit(main(sys.argv))
