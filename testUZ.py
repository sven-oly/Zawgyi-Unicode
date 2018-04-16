#!/usr/bin/env python
# -*- coding: utf-8 -*-

import transliterate
import translit_normalizeZ
import translit_unicode2zawgyi

import difflib

import sys


uz_converter = None


def runTests(debug):
  testdata = translit_unicode2zawgyi.TestData()

  index = 0
  passing = []
  failing = []
  for test_num, expected, input in testdata:
    print
    print '-'*60
    try:
      print 'Test %2d: %s --> %s' % (test_num, input.encode('utf-8'),
                                     expected.encode('utf-8'))
    except:
      print 'TEST CANNOT PRINT %s' % index

    result = uz_converter.transliterate(input, debug)
    expected_normalized = z_normalizer.transliterate(expected, debug)

    if result == expected_normalized:
      print 'PASS %s: in=%s, result=%s, expected = %s' % (index, input.encode('utf-8'),
                                                                result.encode('utf-8'),
                                                                expected.encode('utf-8'))
      passing.append(index)
    else:
      print 'FAIL: %s: in=%s, result=%s, expected = %s' % (index, input.encode('utf-8'),
                                                                result.encode('utf-8'),
                                                                expected.encode('utf-8'))
      print '  result:   %s\n  expected: %s' % (
          transliterate.uStringToHex(result).split(),
          transliterate.uStringToHex(expected).split()
      )

      failing.append(index)

    index += 1

  print 'FAIL = %s' % failing
  print 'PASS = %s' % passing


def resultsDiff(a, b):
  d = difflib.Differ()
  diff = d.compare(a, b)
  print '\n'.join(diff)


def main(args):
  global uz_converter
  global z_normalizer

  debug = True
  if len(args) > 2:
    debug = True
  uz_converter = transliterate.Transliterate(
      translit_unicode2zawgyi.UNICODE_ZAWGYI_TRANSLITERATE,
      translit_unicode2zawgyi.UZ_description)

  z_normalizer = transliterate.Transliterate(
      translit_normalizeZ.TRANS_LIT_RULES,
      translit_normalizeZ.Description)

  print 'RULES FOR %s' % translit_unicode2zawgyi.UZ_description

  uz_converter.summary(show_rules=False)

  runTests(debug)


if __name__ == "__main__":
    print 'ARGS = %s' % sys.argv
    sys.exit(main(sys.argv))
