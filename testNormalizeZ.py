#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Tests conversion from Zawgyi to Unicode.
import transliterate
import translit_normalizeZ

import difflib

import sys


z_normalizer = None


def runTests():
  testdata = translit_normalizeZ.TestData()

  debug = False
  index = 0
  passing = []
  failing = []
  for test_num, input, expected, comment in testdata:
    print
    print '-'*60
    try:
      print 'Test %s "%s": %s --> %s' % (test_num, comment,
                                          input.encode('utf-8'),
                                          expected.encode('utf-8'))
    except:
      print 'TEST CANNOT PRINT %s' % index

    result = z_normalizer.transliterate(input, debug)
    if result == expected:
      print 'PASS %s: in=%s, result=%s, expected = %s' % (test_num, input.encode('utf-8'),
                                                                result.encode('utf-8'),
                                                                expected.encode('utf-8'))
      passing.append(test_num)
    else:
      print 'FAIL: %s: in=%s, result=%s, expected = %s' % (test_num, input.encode('utf-8'),
                                                                result.encode('utf-8'),
                                                                expected.encode('utf-8'))
      print '  result:   %s\n  expected: %s' % (
          transliterate.uStringToHex(result),
          transliterate.uStringToHex(expected)
      )
      resultsDiff(
          transliterate.uStringToHex(result),
          transliterate.uStringToHex(expected)
      )
      failing.append(test_num)

    index += 1

  print 'FAIL = %s' % failing
  print 'PASS = %s' % passing


def resultsDiff(a, b):
  d = difflib.Differ()
  diff = d.compare(a, b)
  # TODO(ccornelius): print out the differences succintly.


def main(args):
  global z_normalizer

  z_normalizer = transliterate.Transliterate(
      translit_normalizeZ.TRANS_LIT_RULES,
      translit_normalizeZ.Description)

  print 'RULES FOR %s' % translit_normalizeZ.Description

  z_normalizer.summary(show_rules=True)

  runTests()


if __name__ == "__main__":
    print 'ARGS = %s' % sys.argv
    sys.exit(main(sys.argv))
