#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re
import sys

MYAZEDI_description = 'Transliteration rules for Myazedi to Unicode'
MYAZEDI_UNICODE_TRANSLITERATE = u"""# Modern Burmese digits & Unicode code points.
$nondigits = [^\u1040-\u1049];
$space = '\u0020';
$consonant = [\u1000-\u1021];
$vowelsign = [\u102B-\u1030\u1032];
$umedial = [\u103B-\u103E];
$vowelmedial = [\u102B-\u1030\u1032\u103B-\u103F];
$ukinzi = \u1004\u103A\u1039;
$myazedi_medialra = [\u1033\u1034\u1090-\u1093];

# #### STAGE (1): CODEPOINT MAPPING FROM Myazedi TO UNICODE
($consonant) \u1086 > $ukinzi $1;
($consonant) \u1035 > $1 \u103B;

# Ignore inserted invisible spaces
\u200b > ;

\u103C \u108A > \u103D \u103E;
\u103C > \u103D ;  # Rule 24
\u103D > \u103E ;   # Rule 26

\u1039 > \u103A ;
\u1033 > \u103C ;
\u1034 > \u103C ;
\u1035 > \u103b;
\u105D > \u102B ;
\u105E > \u102B \u103A ;
\u105F > \u103E ;

\u1031 \u1094 ($consonant) \u103D > $1 \u103E \u1031 \u1037 ;

\u1060 > \u1039 \u1000 ;
\u1061 > \u1039 \u1001 ;
\u1062 > \u1039 \u1002 ;
\u1063 > \u1039 \u1003 ;
\u1064 > \u1039 \u1005 ;
\u1065 > \u1039 \u1006 ;
\u1066 > \u1039 \u1007 ;
\u1067 > \u1039 \u100f ;
[\u1068\u1069] > \u1039 \u1010 ;
[\u106a\u106b] > \u1039 \u1011 ;
\u106C > \u1039 \u1012 ;
\u106D > \u1039 \u1013 ;
\u106E > \u1039 \u1014 ;
\u106F > \u1039 \u1015  ;

\u1070 > \u1039 \u1016 ;
\u1071 > \u1039 \u1017 ;
\u1072 > \u1039 \u1018 ;
\u1073 > \u1039 \u1019 ;
\u1074 > \u1039 \u101c ;
\u1075 > \u1039 \u100c ;
\u1076 > \u1039 \u100b ;
\u1077 > \u1039 \u1010 \u103d;
\u1078 > \u100f \u1039 \u100d ;
\u1079 > \u100d \u1039 \u100e ;
\u107A > \u1039 \u1000 ;
\u107B > \u1039 \u1003 ;
\u107C > \u1039 \u101E ;
\u107D > \u1039 \u1006 ;
\u107F > \u103D \u103E ;
\u107E > \u103D ;

\u1080 > \u103e ;
\u1081 > \u103e \u102f ;
\u1082 > \u102f ;
\u1083 > \u1030 ;
($consonant) \u1084 > $1 \u1036 \u102d;
($consonant) \u1085 > $ukinzi $1 \u1036;
($consonant) \u1086 > $ukinzi $1;
($consonant) \u1087 > $ukinzi $1 \u102d;
($consonant) \u1088 > $ukinzi $1 \u102e;
\u1087 > \u103E ;
\u1088 > \u103E \u102F ;
\u1089 > \u100b  ;
\u108A > \u100b \u1039 \u100b ;
\u108B > \u100d \u1039 \u100d ;
\u108C > \u100a ;
\u108D > \u1039 \u103f ;
\u108E > \u1014 ;
\u108F > \u1025 ;

[\u1090-\u1093] > \u103c ;
[\u1094\u1095] ($consonant)> $1 \u103c\u103d ;
\u1096 > \u103b \u103e;
\u1097 > \u103b \u103d;
\u1098 > \u103b \u103d \u103e;
\u1099 > \u1039 \u1005 \u103b;
[\u109a\u109b] > \u1037;
\u109c > \u1039 \u100f ;
\u109d > \u1039 \u1018 ;
\u109e > \u1039 \u101c ;
\u109f > \u101b ;


#\u1097 ($consonant) > $1 \u103b\u103d ;

##### STAGE (2): POST REORDERING RULES FOR UNICODE RENDERING
::Null;
\u1044 \u103a > | \u104E \u103A ;
($nondigits) \u1040 ([\u102B-\u103F]) > $1 \u101D $2;
#([\u0020\u00A0\u104A\u104b]) \u1031 ($consonant) > $1 $2 \u1031;
\u1031 \u1040 ($nondigits) > \u1031 \u101D $1;
\u1025 \u103A > \u1009 \u103A;
\u1025 \u102E > \u1026;
\u1037\u103A > \u103A\u1037;
\u1036 ($umedial*) ($vowelsign+) > $1 $2 \u1036 ;
([\u102B\u102C\u102F\u1030]) ([\u102D\u102E\u1032]) > $2 $1;
\u103C ($consonant) > $1 \u103C;
##### Stage 3
::Null;
(\u1031) $ukinzi ($consonant) > $ukinzi $2 $1;
\u1031 ($consonant) ($umedial+) > $1 $2 \u1031;
# MAYTBE FIX THIS FOR CURSOR POSITION
\u1031 ($consonant) ([^\u103B-\u103E]) > $1 \u1031 $2;

\u103C \u103A \u1039 ($consonant) > \u103A \u1039 $1 \u103C;
\u1036 ($umedial+) > $1 \u1036;
##### Stage 4
::Null;
([\u103C\u103D\u103E]+) \u103B > \u103B $1;
([\u103D\u103E]+) \u103C > \u103C $1;
\u103E\u103D > \u103D\u103E ;
(\u1031+) ($vowelsign*) \u1039 ($consonant) > \u1039 $3 $1 $2;
($vowelsign+) \u1039 ($consonant) > \u1039 $2 $1;
($umedial) ([\u1031]+) ($umedial*) > $1 $3 $2;
\u1037 ([\u102D-\u1030\u1032\u1036]) > $1 \u1037;
\u1037 ($umedial+) > $1 \u1037;
($vowelsign+) ($umedial+) > $2 $1;
($consonant) ([\u102B-\u1032\u1036\u103B-\u103E]) \u103A ($consonant)> $1 \u103A $2 $3;
##### Stage 5.  More reorderings
::Null;
([\u1031]+) ($umedial+) > $2 $1;
($vowelsign) ($umedial) > $2 $1;
([\u103C\u103D\u103E]) \u103B > \u103B $1;
([\u103D\u103E]) \u103C > \u103C $1;
\u103E\u103D > \u103D\u103E ;
\u1038 ([\u103B\u103C\u103D\u103E]+) > $1 \u1038;
\u1038 ([$vowelmedial]) > $1 \u1038;
\u1038 ([\u1036\u1037\u103A]) > $1 \u1038;
#### Stage 6
::Null;
($consonant) \u103B \u103A > $1 \u103A \u103B;
([\u103C\u103D\u103E]) \u103B > \u103B $1;
([\u103D\u103E]) \u103C > \u103C $1;
\u103E\u103D > \u103D\u103E ;
([\u102D-\u1030\u1032]) \u103A ($consonant) \u103A > $1 $2 \u103A;
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
#
#Try to correctly render diacritics after a space.
#
$space([\u102e\u1037\u103a]) > \u00A0 $1 ;
"""

# (English word, encoded, Unicode)
# See http://my.duniakitab.com/ThanLwinSoft/ThanLwinSoft/MyanmarUnicode/Conversion/myanmarConverter.php
testStrings = [
  (u'cat', 'a=umif', u'ကြောင်'),
  (u'man', 'a,musf', u'ယောက်ျ'),
  (u'woman', 'rdef;r', u'မိန်းမ'),
  (u'university', 'wuUokdvf', u'တက္ကသိုလ်'),
  (u'democracy', "'Drkdua&pD 0g'", 'ဒီမိုကရေစီ ဝါဒ'),
  (u'universal', 'tjynfjynfqkdif&m vl@tcGifhta&; a=unmpmwrf;',
	u'အပြည်ပြည်ဆိုင်ရာ လူ့အခွင့်အရေး ကြေညာစာတမ်း')
  ]