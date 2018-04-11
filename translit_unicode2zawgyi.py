#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

# Unicode Myanmar to Zawgyi converter (prototype)

Description = UZ_description = u'Unicode to Zawgyi conversion'

UNICODE_ZAWGYI_TRANSLITERATE = u"""# Modern Burmese digits & Unicode code points.
$nondigits = [^\u1040-\u1049];
$space = '\u0020';
$consonant = [\u1000-\u1021];
$narrowconsonant = [\u1001\u1002\u1004\u1005\u1007\u100b-\u100e\u1012\u1013\u1015-\u1017\u1019\u101d\u1020\u1025\u1026];
$widenya = [\u100a\u106b];
$othernya = [\u1009\u106a];
$wideconsonant = [\u1000\u1003\u1006\u1009\u100a\u100f\u1010\u1011\u1018\u101c\u101e\u101f\u1021];
$vowelsign = [\u102B-\u1030\u1032];
$vowelmedial = [\u102B-\u1030\u1032\u103B-\u103F];
$ukinzi = \u1004\u103A\u1039;
$spaces = [\u0020\u00a0\u2000-\u200a];

$medialraZ = [\u103b\u107e-\u1084];
$lowsignZ = [\u102f\u1030\u1033\u1034\u1037\u103a\u103c\u103d\u1087-\u108a];
$highsignZ = [\u102d\u102e\u1032\u1036\u1039\u103d-\u103e];

### TO FINISH: actually implement U-->Z.

# #### STAGE 0: CODEPOINT MAPPING FROM UNICODE TO ZAWGYI
$ukinzi ($consonant) \u103B > $1 \u103A \u1064 ;

$ukinzi ($consonant) \u102D \u1036 > $1 \u108e ;

$ukinzi ($consonant) \u102D > $1 \u108b ;
$ukinzi ($consonant) \u102E > $1 \u108C ;

$ukinzi ($consonant) \u1036 > $1 \u108D ;

$ukinzi ($consonant) \u103B \u102D \u102F > $1 \u103A \u1033 \u108B ;
$ukinzi ($consonant) \u103B \u102D > $1 \u103A \u108b  ;
$ukinzi ($consonant) \u103B \u102E \u102F > $1 \u103A \u108C \u1033 ;
$ukinzi ($consonant) \u103B \u102E > $1 \u103A \u108C ;
$ukinzi ($consonant) \u103B \u1036 > $1 \u103A \u108D ;

$ukinzi \u102D > \u108B ;
$ukinzi \u102E  > \u108C  ;
$ukinzi \u1036 > \u108D  ;

$ukinzi ($consonant) > $1 \u1064 ;

$ukinzi > \u1064 ;

\u1025 ($vowelsign) \u1038  > \u106A $1 \u1038 ;

# E Vowel
($narrowconsonant) \u103c \u1031 > \u1031 \u103b $1 ;
($wideconsonant) \u103c \u1031 >  \u1031 \u107e $1;

($consonant) \u103E \u1031 \u1037 > \u1031 \u1094 $1 \u103D ;
($consonant) \u103E \u1031 > \u1031 $1 \u103D ;
($consonant) \u1031 > \u1031 $1 ;

# Medial Ra
($narrowconsonant) \u103c > \u103b $1 ;
($wideconsonant) \u103c > \u107e $1;

\u103F > \u1086 ;
\u103B > \u103A ;  # TODO: Consider context?
\u103C > \u103B ;  # TODO: Needs more context with the base consonants and modifiers

($consonant) \u103d > $1 \u103c;

\u103D > \u103C ;

\u103e \u102f > \u1088 ;

([\u1019]) \u103e \u1030 > $1 \u103d \u1034;  # A special case with signs.

\u103E \u1030 > \u1089 ;

\u103E  > \u103D ;

\u103E \u1030 > \u1089 ;

# \u103E > \u1087 ;  # Is this ever used?

\u103A > \u1039 ;

\u102B \u103A > \u105A ;

\u102D \u1036 > \u108E ;


# \u1037 > \u1094 ;  # Or 1095, depending on the width of the consonant.

\u1025 \u1079 > \u1009 \u1039 \u1016 ;

\u1039 \u1010 \u103d > \u1096 ; # Very special case

\u1039 \u1000 > \u1060 ;
\u1039 \u1001 > \u1061 ;
\u1039 \u1002 > \u1062 ;
\u1039 \u1003 > \u1063 ;
\u1039 \u1005 > \u1065 ;
\u1039 \u1006 > \u1066 ;
\u1039 \u1006 > \u1067 ;
\u1039 \u1007 > \u1068 ;
\u1039 \u1008 > \u1069 ;
\u1039 \u100B > \u106C ;
\u1039 \u100C > \u106D ;
\u1039 \u100F > \u1070 ;
\u1039 \u1010 > \u1071 ;
\u1039 \u1010 > \u1072 ;
\u1039 \u1010 \u103D> \u1096 ;
\u1039 \u1011 > \u1073 ;
\u1039 \u1011 > \u1074 ;
\u1039 \u1012 > \u1075 ;
\u1039 \u1013 > \u1076 ;
\u1039 \u1014 > \u1077 ;
\u1039 \u1015 > \u1078 ;
\u1039 \u1016 > \u1079 ;
\u1039 \u1017 > \u107A ;
\u1039 \u1018 > \u107B ;
\u1039 \u1018 > \u1093 ;
\u1039 \u1019 > \u107C ;
\u1039 \u101C > \u1085 ;

\u1039\u100D > \u106E ;
\u1039\u100E > \u106F ;

\u100F\u1039\u100D > \u1091 ;
\u100B\u1039\u100C > \u1092 ;
\u100B\u1039\u100B > \u1097 ;
\u104E\u1004\u103A\u1038 > \u104E ;

\u102D \u1036 > \u108E  ;


##### STAGE 1: Everything is not in Zawgyi code points. REORDERING RULES.
::Null;

# Handle Na with lower modifiers.
\u1014 ($lowsignZ) \u1037 > \u108f $1 \u1094;
\u1014 ([\u1032]*) \u1037 > \u1014 $1 \u1094;

\u1014 ($lowsignZ) > \u108f $1;

# TODO: Move 1037 dot to right with other descenders.
($lowsignZ) ($highsignZ*)\u1037 > $1 $2 \u1094;

($nondigits) \u1040 ([\u102B-\u103F]) > $1 \u101D $2;
\u1031 \u1040 ($nondigits) > \u1031 \u101D $1;
\u1025 \u103A > \u1009 \u103A;
\u1025 \u102E > \u1026;
\u1037 \u103A > \u103A \u1037;

([\u102B\u102C\u102F\u1030]) ([\u102D\u102E\u1032]) > $2 $1;


# Replace some 1037s.
# ($wideconsonant) \u1037 > $1 \u1094 ;  ## IS THIS RIGHT?

# Some composed lower output
\u103c \u103d > \u108a ;

# Medial plus vowel sign U
($medialraZ) ($consonant) \u102f > $1 $2 \u1033;

## Stage 2: Further adjustments
::Null;

\u103c \u1094 > \u103c \u1095 ;  ## ?? Is this correct?

# Medial ra variations
$medialraZ ($narrowconsonant) ($lowsignZ) ($highsignZ) > \u1083 $1 $2 $3 ;
$medialraZ ($wideconsonant) ($lowsignZ) ($highsignZ) > \u1084 $1 $2 $3 ;

$medialraZ ($narrowconsonant) ($highsignZ) > \u107f $1 $2 ;
$medialraZ ($wideconsonant) ($highsignZ) > \u1080 $1 $2 ;

$medialraZ ($narrowconsonant) ($lowsignZ) > \u1081 $1 $2 ;
$medialraZ ($wideconsonant) ($lowsignZ) > \u1082 $1 $2 ;

$medialraZ ($widenya) > \u1082 $1 ;
$medialraZ ($othernya) > \u103b \u106a ;

$medialraZ ($narrowconsonant) > \u103b $1 ;
$medialraZ ($wideconsonant) > \u107e $1 ;

\u100A ($lowsignZ)> \u106B $1  ;  ## NYA and NNYA

\u103d \u102d > \u102d \u103d;

\u103a ($highsignZ) \u102f [\u1037\u1094\u1095] > \u103a $1 \u1033 \u1095;
\u103a \u102f [\u1037\u1094\u1095] > \u103a \u1033 \u1095;

\u103a \u102f > \u103a \u1033;

##### Stage 3
::Null;
([\u103C\u103D\u103E]+) \u103B > \u103B $1;
([\u103D\u103E]+) \u103C > \u103C $1;
\u103E\u103D > \u103D\u103E ;

\u1039 ($consonant) \u1031 ($vowelsign*) > \u1031 $2 \u1039 $1 ;  # U => Z

# TODO: Is this important?
# ($vowelsign+) \u1039 ($consonant) > \u1039 $2 $1;

\u1037 ([\u102D-\u1030\u1032\u1036]) > $1 \u1037;
($consonant) ([\u102B-\u1032\u1036\u103B-\u103E]) \u103A ($consonant)> $1 \u103A $2 $3;

# Combine vowel and consonant signs
\u103d \u102f > \u1088;

\u1033 \u1094 > \u1033 \u1095; # Wider spacing on lower dot

($medialraZ) ($consonant) ($highsignZ) \u102f > $1 $2 $3 \u1033;


##### Stage 4.  More reorderings
::Null;

([\u103C\u103D\u103E]) \u103B > \u103B $1;
([\u103D\u103E]) \u103C > \u103C $1;
\u103E\u103D > \u103D\u103E ;
\u1038 ([$vowelmedial]) > $1 \u1038;
\u1038 ([\u1036\u1037\u103A]) > $1 \u1038;

\u1036 \u102f > \u102f \u1036;

#### Stage 5
::Null;
($consonant) \u103B \u103A > $1 \u103A \u103B;
([\u103C\u103D\u103E]) \u103B > \u103B $1;
([\u103D\u103E]) \u103C > \u103C $1;
\u103E\u103D > \u103D\u103E ;
([\u102D-\u1030\u1032]) \u103A ($consonant) \u103A > $1 $2 \u103A;
\u102D \u103A > \u102D;
\u102E \u103A > \u102E;
\u102F \u103A > \u102F;
\u102D \u102E > \u102E;
\u102F \u1030 > \u102F;
\u102B \u102B+ > \u102B;
\u102C \u102C+ > \u102C;
\u102D \u102D+ > \u102D;
\u102E \u102E+ > \u102E;
\u102F \u102F+ > \u102F;
\u1030 \u1030+ > \u1030;
\u1031 \u1031+ > \u1031;
\u1032 \u1032+ > \u1032;
\u103A \u103A+ > \u103A;
\u103B \u103B+ > \u103B;
\u103C \u103C+ > \u103C;
\u103D \u103D+ > \u103D;
\u103E \u103E+ > \u103E;

\u1036 \u1036+ > \u1036;

# \u102D \u102f > \u102f \u102D; # This can go either way
\u102f \u1036 > \u1036 \u102f ;  # These are visually identical
\u1039 \u1037 > \u1037 \u1039 ;  # These are visually identical
\u103c \u1032 > \u1032 \u103c ;  # These are visually identical 
\u103c \u102e > \u102e \u103c ;  # These are visually identical 

#
"""

date_entered = '27-Mar-2018'
description = 'First try for transliteration rules for Unicode to Zawgyi'

def printRules():
  print 'Rules for %s' % Description
  lines = UNICODE_ZAWGYI_TRANSLITERATE.split('\n')
  ruleNum = 0
  for line in lines:
    line = line.strip()
    if len(line) > 0 and line[0] != '#':
      print ('%4d\t%s' % (ruleNum, line))
      ruleNum += 1

def TestData():
  # Test data, partly manufactured, to check on the various conversion
  # issues for Unicode to a form of Zawgyi
  test_samples_U2Z = [
      [0, u'ၾက', u'ကြ'],
      [1, u'ႏြးသြားမယ္လို႔ လူ', u'နွးသွားမယ်လို့ လူ'],
      [2, u'ၿငိမ္းခ်မ္းေရးလမ္းေၾကာင္းအျဖစ္', u'ငြိမ်းချမ်းရေးလမ်းကြောင်းအဖြစ်'],
      [3, u'အေျခအျမစ္မရွိဘဲ', u'အခြေအမြစ်မရှိဘဲ'],
      [4,u'ပာၾကားလုိက္ပါတယ္။', u'ပာကြားလိုက်ပါတယ်။'],
      [5, u'ဒီအေၾကာင္း အခမ္းအနားမွာ', u'ဒီအကြောင်း အခမ်းအနားမှာ'],
      [6, u'ကာကြယ္ေရးဦးစီးခ်ဳပ္ ဗုိလ္ခ်ဳပ္မႉးႀကီး', u'ကာကွယ်ရေးဦးစီးချုပ် ဗိုလ်ချုပ်မှူးကြီး'],
      [7,u'လမ္းၫႊန္ေျမပံုပင္ျဖစ္ေၾကာင္း၊', u'လမ်းညွှန်မြေပုံပင်ဖြစ်ကြောင်း၊'],
      [8, u'ဂုဏ္ျပဳ ညစာစားပြဲနဲ႔', u'ဂုဏ်ပြု ညစာစားပွဲနဲ့'],
      [9, u'ဧည့္ခံမွာ ျဖစ္ပါတယ္။', u'ဧည့်ခံမှာ ဖြစ်ပါတယ်။'],
      [10, u'ဗုိလ္ခ်ဳပ္မွဴးႀကီးမင္းေအာင္လိႈင္', u'ဗိုလ်ချုပ်မှူးကြီးမင်းအောင်လှိုင်'],
      [11, u'တိုင္းရင္းသားအဖဲြ႔အခ်ိဳ႕လက္မခံ', u'တိုင်းရင်းသားအဖွဲ့အချို့လက်မခံ'],
      [12, u'ၿဖိဳး ၾကာ   ၾကည္း  ေျပာျပခ် ၿမိဳ  ျဖစ္သ', u'ဖြိုး ကြာ   ကြည်း  ပြောပြချ မြို  ဖြစ်သ'],
      [13, u'ရွိေနတဲ့', u'ရှိနေတဲ့'],
      [14, u'ကႊကႋကႌကႍကႎ', u'ကွှင်္ကိင်္ကီင်္ကံကိံ'],
      [15, u'ခႊ ခႋ ခႌ ခႍ ခႎ', u'ခွှ င်္ခိ င်္ခီ င်္ခံ ခိံ'],
      [16, u'ကၪြ ကၫြ ကၬ ကၭ', u'ကဉွ ကညွ က္ဋ က္ဌ'],
      [17, u'ဗိုလ္ခ်ဳပ္မွဴးႀကီးမင္းေအာင္လိႈင္က', u'ဗိုလ်ချုပ်မှူးကြီးမင်းအောင်လှိုင်က'],
      [18, u'ႀကီဳ', u'ကြီု'],
      [19, u'ႀကီ', u'ကြီ'],
      [20, u'ႃခီြ', u'ခြွီ'],
      [21, u'ႄကီြ', u'ကြွီ'],
      [22, u'ႀကီ', u'ကြီ'],
      [23, u'ႂကြ', u'ကြွ'],
      [24, u'ႁခြ', u'ခြွ'],
      [25, u'ၾကျခၿခီ', u'ကြခြခြီ'],
      [26, u'ကၤဂၤ', u'င်္ကင်္ဂ'],
      [27, u'ကၩဂၩ', u'က္ဈဂ္ဈ'],
      [28, u'၎', u'၎င်း'],
      [29, u'ကၠကၡကၢကၣကၥကၦကၧကၨကၬကၭ', u'က္ကက္ခက္ဂက္ဃက္စက္ဆက္ဆက္ဇက္ဋက္ဌ'],
      [30, u'ကၰကၱကၲကၳကၴကၵကၶကၷကၸကၹကၺကၻကၼက႓က႖',
       u'က္ဏက္တက္တက္ထက္ထက္ဒက္ဓက္နက္ပက္ဖက္ဗက္ဘက္မက္ဘက္တွ'],
      [31, u'ႀက္', u'ကြ်'],
      [32, u'ကၤ', u'င်္က'],
      [33, u'ေမွာင္ခုိကုန္သြယ္မႈေၾကာင့္ ျမန္မာႏုိင္ငံနစ္နာဆံုးရႈံးရပံုေတြကို',
       u'မှောင်ခိုကုန်သွယ်မှုကြောင့် မြန်မာနိုင်ငံနစ်နာဆုံးရှုံးရပုံတွေကို'],
      [34 ,u'ဆံုးရႈံးရပံုေတြကို', u'ဆုံးရှုံးရပုံတွေကို'],
      [35, u'လႊတ္ေတာ္ကုိယ္စားလွယ္ေတြက', u'လွှတ်တော်ကိုယ်စားလှယ်တွေက'],
      [36, u'န႔မနက္', u'န့မနက်'],
      [37, u'တ္ေတာ္ကုိ', u'တ်တော်ကို'],
      [38, u'ျၪ ႂည', u'ဉြ ညြ'],
      [39, u' ေသေသခ်ာခ်ာ', u' သေသချာချာ'],  # This one fails on the Z->Unicode conversion
  ]

  return test_samples_U2Z


def runTestCases():

  testdata = TestData()

  for item in testdata:
    input = item[1]
    expected = item[0]
    print input, expected


def main(argv=None):
  #printRules()

  runTestCases()


if __name__ == "__main__":
    print 'ARGS = %s' % sys.argv
    sys.exit(main(sys.argv))
