#!/usr/bin/env python
# -*- coding: utf-8 -*-

import transliterate
import translit_normalizeZ
import translit_unicode2zawgyi

import difflib

import sys


uz_converter = None


def printDiff(a, b):
  # Compare the two strings, character by character.
  alen = len(a)
  blen = len(b)
  print 'ALEN = %s, BLEN = %s' %(alen, blen)
  i = 0
  comp_str = ''
  while (i < min(alen, blen)):
    if a[i] == b[i]:
      add = '.'
    else:
      add = '^'
    comp_str += add
    i += 1

  comp_str += '#' * (max(alen, blen) - i)
  return comp_str


def runOneTest(debug, id):
  # Run the one with the given id in debug mode.
  testdata = translit_unicode2zawgyi.TestData()
  for test_num, expected, input in testdata:
    if test_num != id:
      continue

    result = uz_converter.transliterate(input, debug)
    expected_normalized = z_normalizer.transliterate(expected, debug)
    result_normalized = z_normalizer.transliterate(result, debug)

    if result_normalized == expected_normalized:
      print 'PASS %s: in=%s, result=%s, expected = %s' % (test_num, input.encode('utf-8'),
                                                                result.encode('utf-8'),
                                                                expected.encode('utf-8'))
    else:
      print 'FAIL: %s: in=%s, result=%s, expected = %s' % (test_num, input.encode('utf-8'),
                                                                result.encode('utf-8'),
                                                                expected.encode('utf-8'))
      print '  result:   %s\n  expected: %s' % (
          transliterate.uStringToHex(result),
          transliterate.uStringToHex(expected)
      )

      print '            %s\n' % printDiff(
          transliterate.uStringToHex(result),
          transliterate.uStringToHex(expected)
      )


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
    result_normalized = z_normalizer.transliterate(result, debug)

    if result_normalized == expected_normalized:
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
      print '            %s\n' % printDiff(
          transliterate.uStringToHex(result),
          transliterate.uStringToHex(expected)
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

  debug = 0
  do_one = -1
  if len(args) > 1:
    try:
      debug = int(args[-1])
    except:
      debug = 1

  if len(args) > 2:
    do_one = int(args[1])

  uz_converter = transliterate.Transliterate(
      translit_unicode2zawgyi.UNICODE_ZAWGYI_TRANSLITERATE,
      translit_unicode2zawgyi.UZ_description)

  z_normalizer = transliterate.Transliterate(
      translit_normalizeZ.TRANS_LIT_RULES,
      translit_normalizeZ.Description)

  print 'RULES FOR %s' % translit_unicode2zawgyi.UZ_description

  show_the_rules = False
  if debug > 1:
    show_the_rules = True
  uz_converter.summary(show_rules=show_the_rules)

  if do_one >= 0:
    runOneTest(debug, do_one)
  else:
    runTests(debug)


if __name__ == "__main__":
    print 'ARGS = %s' % sys.argv
    sys.exit(main(sys.argv))
