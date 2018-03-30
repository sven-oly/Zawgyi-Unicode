#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

# Unicode Myanmar to Zawgyi converter (prototype)

Description = UZ_description = u'Unicode to Zawgyi conversion'

UNICODE_ZAWGYI_TRANSLITERATE = u"""# Modern Burmese digits & Unicode code points.
$nondigits = [^\u1040-\u1049];
$space = '\u0020';
$consonant = [\u1000-\u1021];
$vowelsign = [\u102B-\u1030\u1032];
$umedial = [\u103B-\u103E];
$vowelmedial = [\u102B-\u1030\u1032\u103B-\u103F];
$ukinzi = \u1004\u103A\u1039;
$zmedialra = [\u103B\u107E-\u1084];
$spaces = [\u0020\u00a0\u2000-\u200a];

### TO FINISH: actually implement U-->Z.

# #### STAGE (1): CODEPOINT MAPPING FROM UNICODE TO ZAWGYI
$ukinzi ($consonant) \u103B > $1 \u103A \u1064 ;
$ukinzi ($consonant) > $1 \u1064 ;
$ukinzi > \u1064 ;
$ukinzi $$consonant \u102D > $ukinzi $1 \u102D ;
$ukinzi ($consonant) \u102E > $1 \u108C ;

$ukinzi ($consonant) \u1036 > $1 \u108D ;
$ukinzi ($consonant) \u103B \u102D \u102F > $1 \u103A \u1033 \u108B ;
$ukinzi ($consonant) \u103B \u102D > $1 \u103A \u108b  ;
$ukinzi ($consonant) \u103B \u102E \u102F > $1 \u103A \u108C \u1033 ;
$ukinzi ($consonant) \u103B \u102E > $1 \u103A \u108C ;
$ukinzi ($consonant) \u103B \u1036 > $1 \u103A \u108D ;

($consonant) \u103B \u102D \u1036 > $1 \u103A \u108e  ;

$ukinzi \u102D > \u108B ;
$ukinzi \u102E  > \u108C  ;
$ukinzi \u1036 > \u108D  ;

\u1025 ($vowelsign) \u1038  > \u106A $1 \u1038 ;
\u1009 > \u106A  ;
\u100A > \u106B  ;

# Ignore inserted invisible spaces
\u200b > ;

#### !!!!! $zmedialra > \u103c;  # TODO FIX THIS!

u1014 > \u108F ;
u101B > \u1090 ;
u103F > \u1086 ;
\u103B > \u103A ;
\u103C > \u103B  ;  # TODO: Needs more context with the base consonants and modifiers
\u103B > \u107D ;
\u103D \u103E > \u103C \u108A ;

 \u103D  > \u103C ;
 
 
\u103D \u103E > \u108A ;
\u103E  > \u103D > \u103E ;   # Rule 26
 \u103E > \u1087 ;
\u103E \u102F  > \u1088 > ;
\u103E \u1030 > \u1089 > ;
\u103A > \u1039 ;

\u102f > \u102F ;  # U => Z, but may need to be contextual
\u1030 > \u1034 ;

\u102B \u103A > \u105A ;
\u102D \u1036 > \u108E  ;
## TODO: MORE TO DO HERE
\u1031 \u1094 ($consonant) \u103D > $1 \u103E \u1031 \u1037 ;  # U => Z
u1037 > \u1094 ;  # Or 1095, depending on the width of the consonant.

\u1025 \u1061 > \u1009 \u1039 \u1001;
\u1025 \u1062 > \u1009 \u1039 \u1002;
\u1025 \u1065 > \u1009 \u1039 \u1005;
\u1025 \u1068 > \u1009 \u1039 \u1007;
\u1025 \u1076 > \u1009 \u1039 \u1013;
\u1025 \u1078 > \u1009 \u1039 \u1015;
\u1025 \u107A > \u1009 \u1039 \u1017;
\u1025 \u1079 > \u1009 \u1039 \u1016;
\u1060 > \u1039 \u1000 ;
\u1061 > \u1039 \u1001 ;
\u1062 > \u1039 \u1002 ;
\u1063 > \u1039 \u1003 ;
\u1065 > \u1039 \u1005 ;
\u1066 > \u1039 \u1006 ;
\u1067 > \u1039 \u1006 ;
\u1068 > \u1039 \u1007 ;
\u1069 > \u1039 \u1008 ;
\u106C > \u1039 \u100B ;
\u106D > \u1039 \u100C ;
\u1039 \u100F > \u1070 ;  # U => Z
\u1039 \u1010 > \u1071 ;  # U => Z
\u1072 > \u1039 \u1010 ;
\u1096 > \u1039 \u1010 \u103D;
\u1073 > \u1039 \u1011 ;
\u1074 > \u1039 \u1011 ;
\u1075 > \u1039 \u1012 ;
\u1076 > \u1039 \u1013 ;
\u1077 > \u1039 \u1014 ;
\u1078 > \u1039 \u1015 ;
\u1079 > \u1039 \u1016 ;
\u107A > \u1039 \u1017 ;
\u107B > \u1039 \u1018 ;
\u1093 > \u1039 \u1018 ;
\u107C > \u1039 \u1019 ;
\u1085 > \u1039 \u101C ;
\u106E > \u100D\u1039\u100D ;
\u106F > \u100D\u1039\u100E ;
\u1091 > \u100F\u1039\u100D ;
\u1092 > \u100B\u1039\u100C ;
\u1097 > \u100B\u1039\u100B ;
\u104E > \u104E\u1004\u103A\u1038 ;
  
##### STAGE (2): POST REORDERING RULES FOR UNICODE RENDERING
::Null;

($consonant) \u1031 > \u1031 $1 ;  # Put the E vowel back before the consonant.
($consonant) ([\u103d\u103e]) \u1031 > \u1031 $1 $2;  # Put the E vowel back before the consonant.

\u1044 \u103a > | \u104E \u103A ;
($nondigits) \u1040 ([\u102B-\u103F]) > $1 \u101D $2;
\u1031 \u1040 ($nondigits) > \u1031 \u101D $1;
\u1025 \u103A > \u1009 \u103A;
\u1025 \u102E > \u1026;
\u1037\u103A > \u103A\u1037;
\u1036 ($umedial*) ($vowelsign+) > $1 $2 \u1036 ;
([\u102B\u102C\u102F\u1030]) ([\u102D\u102E\u1032]) > $2 $1;
\u103C ($consonant) > $1 \u103C;

# Medial ra before consonant.

##### Stage 3
::Null;
($consonant) \u103b > \u103b $1 ;  # Put the E vowel back before the consonant.


$ukinzi ($consonant) \u1031 > \u1031 $ukinzi $2 ;   # U => Z
 ($consonant) ($umedial+) \u1031  $1 $2 \u1031;  # U => Z
 
($consonant) \1031 ([^\u103B-\u103E]) > \u1031 $1 $2;  # U => Z

\u103C \u103A \u1039 ($consonant) > \u103A \u1039 $1 \u103C;
\u1036 ($umedial+) > $1 \u1036;
##### Stage 4
::Null;
([\u103C\u103D\u103E]+) \u103B > \u103B $1;
([\u103D\u103E]+) \u103C > \u103C $1;
\u103E\u103D > \u103D\u103E ;

\u1039 ($consonant) \u1031 ($vowelsign*) > \u1031 $2 \u1039 $1 ;  # U => Z

($vowelsign+) \u1039 ($consonant) > \u1039 $2 $1;

\u1037 ([\u102D-\u1030\u1032\u1036]) > $1 \u1037;
\u1037 ($umedial+) > $1 \u1037;
($vowelsign+) ($umedial+) > $2 $1;
($consonant) ([\u102B-\u1032\u1036\u103B-\u103E]) \u103A ($consonant)> $1 \u103A $2 $3;

##### Stage 5.  More reorderings
::Null;

($vowelsign) ($umedial) > $2 $1;
([\u103C\u103D\u103E]) \u103B > \u103B $1;
([\u103D\u103E]) \u103C > \u103C $1;
\u103E\u103D > \u103D\u103E ;
\u1038 ([$vowelmedial]) > $1 \u1038;
\u1038 ([\u1036\u1037\u103A]) > $1 \u1038;
# NEW 5-May-2016
\u1036 \u102f > \u102f \u1036;
#### Stage 6
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
# NEW 5-May-2016
\u1036 \u1036+ > \u1036;
#
#Try to correctly render diacritics after a space.
#
($space)([\u102e\u1037\u103a]) > $2 \u00A0;
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

def U2ZTestData():
  # Test data, partly manufactured, to check on the various conversion
  # issues for Unicode to a form of Zawgyi
  test_samples_U2Z = [
    ("ၿငိမ္းခ်မ္းေရးလမ္းေၾကာင္းအျဖစ္", "ငြိမ်းချမ်းရေးလမ်းကြောင်းအဖြစ်"),
    ("အေျခအျမစ္မရွိဘဲ", "အခြေအမြစ်မရှိဘဲ"),
    ("ပာၾကားလုိက္ပါတယ္။", "ပာကြားလိုက်ပါတယ်။"),
    ("ဒီအေၾကာင္း အခမ္းအနားမွာ", "ဒီအကြောင်း အခမ်းအနားမှာ"),
    ("ကာကြယ္ေရးဦးစီးခ်ဳပ္ ဗုိလ္ခ်ဳပ္မႉးႀကီး", "ကာကွယ်ရေးဦးစီးချုပ် ဗိုလ်ချုပ်မှူးကြီး"),
    ("လမ္းၫႊန္ေျမပံုပင္ျဖစ္ေၾကာင္း၊", "လမ်းညွှန်မြေပုံပင်ဖြစ်ကြောင်း၊"),
    ("ဂုဏ္ျပဳ ညစာစားပြဲနဲ႔", "ဂုဏ်ပြု ညစာစားပွဲနဲ့"),
    ("ဧည့္ခံမွာ ျဖစ္ပါတယ္။", "ဧည့်ခံမှာ ဖြစ်ပါတယ်။"),
    ("ဗုိလ္ခ်ဳပ္မွဴးႀကီးမင္းေအာင္လိႈင္", "ဗိုလ်ချုပ်မှူးကြီးမင်းအောင်လှိုင်"),
    ("တိုင္းရင္းသားအဖဲြ႔အခ်ိဳ႕လက္မခံ", "တိုင်းရင်းသားအဖွဲ့အချို့လက်မခံ"),
    ("ၿဖိဳး ၾကာ   ၾကည္း  ေျပာျပခ် ၿမိဳ  ျဖစ္သ", "ဖြိုး ကြာ   ကြည်း  ပြောပြချ မြို  ဖြစ်သ"),
    ("က႔က႕", "က့က့"),
    ("ကႊကႋကႌကႍကႎ", "ကွှင်္ကိင်္ကီင်္ကံကိံ"),
    ("ခႊ ခႋ ခႌ ခႍ ခႎ", "ခွှ င်္ခိ င်္ခီ င်္ခံ ခိံ"),
    ("ကၪ ကၫ ကၬ ကၭ", "ကဉ ကည က္ဋ က္ဌ"),
    ("ဗိုလ္ခ်ဳပ္မွဴးႀကီးမင္းေအာင္လိႈင္က", "ဗိုလ်ချုပ်မှူးကြီးမင်းအောင်လှိုင်က"),
    ("ႄကီ", "ကြီု"),
    ("ႀကီ", "ကြီ"),
    ("ႃခီြ", "ခြွီ"),
    ("ႄကီြ", "ကြွီ"),
    ("ႀကီ", "ကြီ"),
    ("ႂကြ", "ကြွ"),
    ("ႁခြ", "ခြွ"),
    ("ၾကျခၿခီ", "ကြခြခြီ"),
    ("ကၤဂၤ", "င်္ကင်္ဂ"),
    ("ကၩဂၩ", "က္ဈဂ္ဈ"),
    ("၎", "၎င်း"),
    ("ကၠကၡကၢကၣကၥကၦကၧကၨကၬကၭ", "က္ကက္ခက္ဂက္ဃက္စက္ဆက္ဆက္ဇက္ဋက္ဌ"),
    ("ကၰကၱကၲကၳကၴကၵကၶကၷကၸကၹကၺကၻကၼက႓က႖",
     "က္ဏက္တက္တက္ထက္ထက္ဒက္ဓက္နက္ပက္ဖက္ဗက္ဘက္မက္ဘက္တွ"),
    ("ႀက္", "က်ြ "),
  ]

  return test_samples_U2Z


def main(argv=None):
  printRules()


if __name__ == "__main__":
    print 'ARGS = %s' % sys.argv 
    sys.exit(main(sys.argv))
