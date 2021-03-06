#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

# Zawgyi font normalization - reorder to be consistend

Description = ZAWGYI_NORM_description = u'Zawgyi font normalizatoin'

TRANS_LIT_RULES = ZAWGYI_NORMALIZE_TRANSLITERATE = u"""
\u1025 \u102e > \u1026 ;

\u102f ([\u102d\u1036]) > $1 \u102f ;

\u1039 \u1037 > \u1037 \u1039 ;

\u103c ([\u102e\u1032]) > $1 \u103c ;

\u1033 \u102d > \u102d \u1033 ;

\u103d \u102d > \u102d \u103d ;

\u1089 > \u103d \u1034 ;

# Kinzi and others
\u1064 \u103a > \u103a \u1064 ;

# Similar subscripted consonants.
\u1067 > \u1066;
\u1072 > \u1071;
\u1074 > \u1073;
\u1093 > \u107b;

\u1095 > \u1094 ;

# Phase 1. Handle duplicate codes.
::Null;
\u102f+ > \u102f;
\u1039+ > \u1039;
"""

test_data = [
  [39, u'ေသေသခ်ာခ်ာ', u'ေသေသခ်ာခ်ာ', 'no change expected'],
  [3, u'အေျခအျမစ္မရွိဘဲ', u'အေျခအျမစ္မရိွဘဲ', '103d-102d swap'],
  [4, u'ပာၾကားလုိက္ပါတယ္။', u'ပာၾကားလိုက္ပါတယ္။', '102f-102d swap'],
  [6, u'ကာကြယ္ေရးဦးစီးခ်ဳပ္ ဗုိလ္ခ်ဳပ္မႉးႀကီး', u'ကာကြယ္ေရးဦးစီးခ်ဳပ္ ဗိုလ္ခ်ဳပ္မွဴးႀကီး', '1025 102e -> 1026'],
  [8, u'ဂုဏ္ျပဳ ညစာစားပြဲနဲ႔', u'ဂုဏ္ျပဳ ညစာစားပဲြနဲ႔', 'possible bug in converter'],
  [8.1, u'ညစာစားပြဲနဲ', u'ညစာစားပဲြႏဲ့', '1014 conversion'],
  [10, u'ဗုိလ္ခ်ဳပ္မွဴးႀကီးမင္းေအာင္လိႈင္', u'ဗိုလ္ခ်ဳပ္မွဴးႀကီးမင္းေအာင္လိႈင္', '102f-102d swap' ],
  [13, u'ရွိေနတဲ့', u'ရိွေနတဲ့', '103d-102d swap'],
  [16, u'ကၪြ ကၫြ ကၬ ကၭ', u'ကၪြ ကၫြ ကၬ ကၭ', '106a vs 1009 - possible issue'],
  [29, u'ကၠကၡကၢကၣကၥကၦကၧကၨကၬကၭ', u'ကၠကၡကၢကၣကၥကၦကၦကၨကၬကၭ', 'artificial placement of subscript'],
  [30, u'ကၰကၱကၲကၳကၴကၵကၶကၷကၸကၹကၺကၻကၼက႓က႖',
   u'ကၰကၱကၱကၳကၳကၵကၶကၷကၸကၹကၺကၻကၼကၻက႖', 'placement of subscripts'],
  [33, u'ေမွာင္ခုိကုန္သြယ္မႈေၾကာင့္ ျမန္မာႏုိင္ငံနစ္နာဆံုးရႈံးရပံုေတြကို',
   u'ေမွာင္ခိုကုန္သြယ္မႈေၾကာင့္ ျမန္မာနိုင္ငံနစ္နာဆံုးရႈံးရပံုတြေကို', 'swapping?'],
  [33.1, u'ျမန္မာႏုိင္ငံနစ္နာဆံုးရႈံးရပံုေတြကို',
   u'ျမန္မာနိုင္ငံနစ္နာဆံုးရႈံးရပံုတြေကို', 'swapping?'],
  [33.2, u'နာဆံုးရႈံးရပံုေတြကို',
   u'နာဆံုးရႈံးရပံုတြေကို', 'swapping?'],
  [34, u'ဆံုးရႈံးရပံုေတြကို', u'ဆံုးရႈံးရပံုေတြကို', ''],
  [35, u'လႊတ္ေတာ္ကုိယ္စားလွယ္ေတြက', u'လႊတ္ေတာ္ကိုယ္စားလွယ္ေတြက', ''],
  [37, u'တ္ေတာ္ကုိ', u'တ္ေတာ္ကို', ''],
  [8.1, u'ဂုဏ္ျပဳပျပဴဃၾကဴ', u'ဂုဏ္ျပဳပျပဴဃၾကဴ', 'modification of case 8'],
  [40, u'ပံုေတြကို', u'ပံုေတြကို', 'Mod of case 33',],
  [43, u'အတာသႀကၤန္ပြဲေတာ္နဲ', u'အတာသင်္ကြန်ပွဲတော်နဲ', 'kinzi + medial ra'],
]

def TestData():
  return test_data


def main(argv=None):
  return


if __name__ == "__main__":
    print 'ARGS = %s' % sys.argv
    sys.exit(main(sys.argv))
