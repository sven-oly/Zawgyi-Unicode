#!/usr/bin/env python
# -*- coding: utf-8 -*-

# To compare Myanmar text versions to see differences between conversions.
# E.g., to check Unicode vs. conversion from Zawgyi or Myazedi.

import logging
import re
import sys

import difflib

class compareMy():

  def __init__(self, text1=None, text2=None):
    self.text1 = text1
    self.text2 = text2

  def setText(self, t1, t2):
    self.text1 = t1
    self.text2 = t2
      
  def compare(self):
    #contextDiff = difflib.context_diff(self.text1, self.text2, lineterm='')
    #contextDiff = difflib.unified_diff(self.text1, self.text2)

    d = difflib.Differ()
    contextDiff = d.compare(self.text1, self.text2)

    return contextDiff
    

def T0(comparer):
  # Tests with two identical strings.
  t1 = u"""ကျွန်ုပ် တို့ ၏ ပျော် ရွှင် မှု၊ သာယာဝပြော မှု နှင့် အောင်မြင် မှု တို့ သည် ကျွန်ုပ် တို့
၏ ကျန်းမာ ခြင်း အပေါ် တွင် အများ ကြီး မှီခို နေ ပါ သည်။ ပညာတတ် ရန်၊ ကြွယ်ဝ ချမ်းသာ ရန် နှင့် 
ကြိုးပမ်း လုပ်ဆောင် မှု အားလုံး အောင်မြင် စေရန် အတွက် ကျန်းမာရေး သည် အထူး ပင် အရေးကြီး ပါ 
သည်။ ကျန်းမာရေး မ ပြည့်စုံ လျှင် ကျွန်ုပ် တို့ ၏ ပညာရေး၊ စီးပွားရေး မြှင့်တင် မှု လုပ်ငန်း များ 
လုပ် နိုင် လိမ့်မည် မ ဟုတ် ပါ။ သို့ဖြစ်၍ အစဉ်သဖြင့် ကျန်းမာ နေ ရန် ကျွန်ုပ် တို့ ကြိုးစား ကြ ရ ပါ မည်။"""
  t2 = t1
  comparer.setText(t1, t2)
  result = comparer.compare()
  print 'T0 gives: %s' % (result)
  for diff in result:
    sys.stdout.write(diff)  #print diff  


def toHex(uText):
  hex = ' '.join(["%04x" % ord(x) for x in uText])
  return hex


def T1(comparer):
  # Tests with two conversions, one from Zawgyi and other from Myazedi.
  t1 = u'က်န်းမာရေး နည်းလမ်း မ မ်ား'
  t2 = u'ကျန်းမာရေး နည်းလမ်း များ'
  
  #comparer.setText(t1, t2)
  print toHex(t1)
  print toHex(t2)
  comparer.setText(toHex(t1), toHex(t2))
  result = comparer.compare()
  print 'T1 gives" %s' % (result)
  negbits = ''
  for diff in result:
    if diff[0] == '-':
      negbits += diff[2]
    else:
      if negbits:
        print '- ' + negbits, 
        negbits = ''
      sys.stdout.write(diff)
  print negbits
       # sys.stdout.write(diff)
  print 


def main(argv=None):
  # Driver for tests.
  comparer = compareMy()
  
  T0(comparer)
  print
  
  T1(comparer)
  
  return
  

if __name__ == "__main__":
    sys.exit(main())
