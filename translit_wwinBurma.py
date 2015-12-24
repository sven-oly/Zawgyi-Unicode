#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re
import sys

mappings = [
  ('! " # $ % & '' ( ) * + , - . /', u'ည ဓ ျှ ွှ ဏ ရ ဒဒ ( ) ဂ ြ ယ - ၏ ၊'), # \x21-\x2f
  ('0 1 2 3 4 5 6 7 8 9 : ; < = > ?', u'၀ ၁ ၂ ၃ ၄ ၅ ၆ ၇ ၈ ၉ ါ် း ြွ ြ ြွ ။'), # \x30-\x3f
  ('@ A B C D E F G H I J K L M N O', u'့ ဗ B ဃ ီ န င်္ ွ ံ ၍ ဲ ု ူ ္န ္ဒ ဥ'), # \x40-\x4f
  ('P Q R S T U V W X Y Z [ \ ] ^ _', u'္စ ္ခ ္မ ှ ဤ ္က ဠ ္တ ဌ ၌ ဇ ဟ ဿ ] ဉ ှု'), # \x50-\x5f
  ('` a b c d e f g h i j k l m n o', u'ဘ္ပ ေ ဘ ခ ိ န ် ါ ့ င ြ ု ူ ာ ည သ'), # \x60-\x6f
  ('p q r s t u v w x y z { | } ~', u'စ ဆ မ ျ အ က လ တ ထ ပ ဖ ဧ ျွ ြ ္ဂ'),
  (u'á é í ó ú à è ì ò ù ä ë ï ö ü ÿ Á É Í Ó Ú Ä Ë Ï Ö Ü Ÿ ã õ Ã Õ â ê î ô û Â Ê Î Ô Û Å å',
   u'á ျွှ í ó ú à è ì ò ù ä ë ï ိံ ü ÿ ဣ ဋ ဥ 〨 Ó Ú ဍ္ဍ Ë ဋ္ဌ Ö Ü Ÿ ã ငိ်္ ဋ္ဋ Õ â ှ î ငီ်္ û Â ဎ ္ထ Ô Û ဎ္ဍ å')
  ]

mapping_rules = 
"""\u0021 > \u100a ;
\u0022 > \u1013 ;
\u0023 > \u103b \u103e ;
\u0024 > \u103d \u103e ;
\u0025 > \u100f ;
\u0026 > \u101b ;
\u0028 > \u1012 \u1012 ;
\u0029 > \u0028 ;
\u002a > \u0029 ;
\u002b > \u1002 ;
\u002c > \u103c ;
\u002d > \u101a ;
\u002e > \u002d ;
\u002f > \u104f ;
\u0030 > \u1040 ;
\u0031 > \u1041 ;
\u0032 > \u1042 ;
\u0033 > \u1043 ;
\u0034 > \u1044 ;
\u0035 > \u1045 ;
\u0036 > \u1046 ;
\u0037 > \u1047 ;
\u0038 > \u1048 ;
\u0039 > \u1049 ;
\u003a > \u102b \u103a ;
\u003b > \u1038 ;
\u003c > \u103c \u103d ;
\u003d > \u103c ;
\u003e > \u103c \u103d ;
\u003f > \u104b ;
\u0040 > \u1037 ;
\u0041 > \u1017 ;
\u0042 > \u0042 ;
\u0043 > \u1003 ;
\u0044 > \u102e ;
\u0045 > \u1014 ;
\u0046 > \u1004 \u103a \u1039 ;
\u0047 > \u103d ;
\u0048 > \u1036 ;
\u0049 > \u104d ;
\u004a > \u1032 ;
\u004b > \u102f ;
\u004c > \u1030 ;
\u004d > \u1039 \u1014 ;
\u004e > \u1039 \u1012 ;
\u004f > \u1025 ;
\u0050 > \u1039 \u1005 ;
\u0051 > \u1039 \u1001 ;
\u0052 > \u1039 \u1019 ;
\u0053 > \u103e ;
\u0054 > \u1024 ;
\u0055 > \u1039 \u1000 ;
\u0056 > \u1020 ;
\u0057 > \u1039 \u1010 ;
\u0058 > \u100c ;
\u0059 > \u104c ;
\u005a > \u1007 ;
\u005b > \u101f ;
\u005c > \u103f ;
\u005d > \u005d ;
\u005e > \u1009 ;
\u005f > \u103e \u102f ;
\u0060 > \u1018 \u1039 \u1015 ;
\u0061 > \u1031 ;
\u0062 > \u1018 ;
\u0063 > \u1001 ;
\u0064 > \u102d ;
\u0065 > \u1014 ;
\u0066 > \u103a ;
\u0067 > \u102b ;
\u0068 > \u1037 ;
\u0069 > \u1004 ;
\u006a > \u103c ;
\u006b > \u102f ;
\u006c > \u1030 ;
\u006d > \u102c ;
\u006e > \u100a ;
\u006f > \u101e ;
\u0070 > \u1005 ;
\u0071 > \u1006 ;
\u0072 > \u1019 ;
\u0073 > \u103b ;
\u0074 > \u1021 ;
\u0075 > \u1000 ;
\u0076 > \u101c ;
\u0077 > \u1010 ;
\u0078 > \u1011 ;
\u0079 > \u1015 ;
\u007a > \u1016 ;
\u007b > \u1027 ;
\u007c > \u103b \u103d ;
\u007d > \u103c ;
\u007e > \u1039 \u1002 ;
\u00e1 > \u00e1 ;
\u00e9 > \u103b \u103d \u103e ;
\u00ed > \u00ed ;
\u00f3 > \u00f3 ;
\u00fa > \u00fa ;
\u00e0 > \u00e0 ;
\u00e8 > \u00e8 ;
\u00ec > \u00ec ;
\u00f2 > \u00f2 ;
\u00f9 > \u00f9 ;
\u00e4 > \u00e4 ;
\u00eb > \u00eb ;
\u00ef > \u00ef ;
\u00f6 > \u102d \u1036 ;
\u00fc > \u00fc ;
\u00ff > \u00ff ;
\u00c1 > \u1023 ;
\u00c9 > \u100b ;
\u00cd > \u1025 ;
\u00d3 > \u3028 ;
\u00da > \u00d3 ;
\u00c4 > \u00da ;
\u00cb > \u100d \u1039 \u100d ;
\u00cf > \u00cb ;
\u00d6 > \u100b \u1039 \u100c ;
\u00dc > \u00d6 ;
\u0178 > \u00dc ;
\u00e3 > \u0178 ;
\u00f5 > \u00e3 ;
\u00c3 > \u1004 \u102d \u103a \u1039 ;
\u00d5 > \u100b \u1039 \u100b ;
\u00e2 > \u00d5 ;
\u00ea > \u00e2 ;
\u00ee > \u103e ;
\u00f4 > \u00ee ;
\u00fb > \u1004 \u102e \u103a \u1039 ;
\u00c2 > \u00fb ;
\u00ca > \u00c2 ;
\u00ce > \u100e ;
\u00d4 > \u1039 \u1011 ;
\u00db > \u00d4 ;
\u00c5 > \u00db ;
\u00e5 > \u100e \u1039 \u100d ;
"""
# 2015-06-17. CWC.
# Just getting started with this. Needs to be finished.
Translit_description = 'Transliteration rules for WwinBurmese to Unicode'
Convert_UNICODE_TRANSLITERATE = u"""# Modern Burmese digits & Unicode code points.

$nondigits = [^\u1040-\u1049];
$space = '\u0020';
$consonant = [\u1000-\u1021];
$vowelsign = [\u102B-\u1030\u1032];
$umedial = [\u103B-\u103E];
$vowelmedial = [\u102B-\u1030\u1032\u103B-\u103F];
$ukinzi = \u1004\u103A\u1039;
$myazedi_medialra = [\u1033\u1034\u1090-\u1093];

# #### STAGE (1): CODEPOINT MAPPING FROM Wwin Burma TO UNICODE
# Mapping rules from above
\u0021 > \u100a ;
\u0022 > \u1013 ;
\u0023 > \u103b \u103e ;
\u0024 > \u103d \u103e ;
\u0025 > \u100f ;
\u0026 > \u101b ;
\u0028 > \u1012 \u1012 ;
\u0029 > \u0028 ;
\u002a > \u0029 ;
\u002b > \u1002 ;
\u002c > \u103c ;
\u002d > \u101a ;
\u002e > \u002d ;
\u002f > \u104f ;
\u0030 > \u1040 ;
\u0031 > \u1041 ;
\u0032 > \u1042 ;
\u0033 > \u1043 ;
\u0034 > \u1044 ;
\u0035 > \u1045 ;
\u0036 > \u1046 ;
\u0037 > \u1047 ;
\u0038 > \u1048 ;
\u0039 > \u1049 ;
\u003a > \u102b \u103a ;
\u003b > \u1038 ;
\u003c > \u103c \u103d ;
\u003d > \u103c ;
\u003e > \u103c \u103d ;
\u003f > \u104b ;
\u0040 > \u1037 ;
\u0041 > \u1017 ;
\u0042 > \u0042 ;
\u0043 > \u1003 ;
\u0044 > \u102e ;
\u0045 > \u1014 ;
\u0046 > \u1004 \u103a \u1039 ;
\u0047 > \u103d ;
\u0048 > \u1036 ;
\u0049 > \u104d ;
\u004a > \u1032 ;
\u004b > \u102f ;
\u004c > \u1030 ;
\u004d > \u1039 \u1014 ;
\u004e > \u1039 \u1012 ;
\u004f > \u1025 ;
\u0050 > \u1039 \u1005 ;
\u0051 > \u1039 \u1001 ;
\u0052 > \u1039 \u1019 ;
\u0053 > \u103e ;
\u0054 > \u1024 ;
\u0055 > \u1039 \u1000 ;
\u0056 > \u1020 ;
\u0057 > \u1039 \u1010 ;
\u0058 > \u100c ;
\u0059 > \u104c ;
\u005a > \u1007 ;
\u005b > \u101f ;
\u005c > \u103f ;
\u005d > \u005d ;
\u005e > \u1009 ;
\u005f > \u103e \u102f ;
\u0060 > \u1018 \u1039 \u1015 ;
\u0061 > \u1031 ;
\u0062 > \u1018 ;
\u0063 > \u1001 ;
\u0064 > \u102d ;
\u0065 > \u1014 ;
\u0066 > \u103a ;
\u0067 > \u102b ;
\u0068 > \u1037 ;
\u0069 > \u1004 ;
\u006a > \u103c ;
\u006b > \u102f ;
\u006c > \u1030 ;
\u006d > \u102c ;
\u006e > \u100a ;
\u006f > \u101e ;
\u0070 > \u1005 ;
\u0071 > \u1006 ;
\u0072 > \u1019 ;
\u0073 > \u103b ;
\u0074 > \u1021 ;
\u0075 > \u1000 ;
\u0076 > \u101c ;
\u0077 > \u1010 ;
\u0078 > \u1011 ;
\u0079 > \u1015 ;
\u007a > \u1016 ;
\u007b > \u1027 ;
\u007c > \u103b \u103d ;
\u007d > \u103c ;
\u007e > \u1039 \u1002 ;
\u00e1 > \u00e1 ;
\u00e9 > \u103b \u103d \u103e ;
\u00ed > \u00ed ;
\u00f3 > \u00f3 ;
\u00fa > \u00fa ;
\u00e0 > \u00e0 ;
\u00e8 > \u00e8 ;
\u00ec > \u00ec ;
\u00f2 > \u00f2 ;
\u00f9 > \u00f9 ;
\u00e4 > \u00e4 ;
\u00eb > \u00eb ;
\u00ef > \u00ef ;
\u00f6 > \u102d \u1036 ;
\u00fc > \u00fc ;
\u00ff > \u00ff ;
\u00c1 > \u1023 ;
\u00c9 > \u100b ;
\u00cd > \u1025 ;
\u00d3 > \u3028 ;
\u00da > \u00d3 ;
\u00c4 > \u00da ;
\u00cb > \u100d \u1039 \u100d ;
\u00cf > \u00cb ;
\u00d6 > \u100b \u1039 \u100c ;
\u00dc > \u00d6 ;
\u0178 > \u00dc ;
\u00e3 > \u0178 ;
\u00f5 > \u00e3 ;
\u00c3 > \u1004 \u102d \u103a \u1039 ;
\u00d5 > \u100b \u1039 \u100b ;
\u00e2 > \u00d5 ;
\u00ea > \u00e2 ;
\u00ee > \u103e ;
\u00f4 > \u00ee ;
\u00fb > \u1004 \u102e \u103a \u1039 ;
\u00c2 > \u00fb ;
\u00ca > \u00c2 ;
\u00ce > \u100e ;
\u00d4 > \u1039 \u1011 ;
\u00db > \u00d4 ;
\u00c5 > \u00db ;
\u00e5 > \u100e \u1039 \u100d ;

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

# Simple print out.
def printMappingRules():
  for m in mappings:
    index = 0
    left = m[0].split()
    right = m[1].split()
    #print '** len(0) = %d, len(1) = %d' % (
    #   len(left), len(right))
    lineout = []
    lineout.append('%s > ' % left)
    i = 0
    for lval in left:
      lineout = []
      lineout.append('\u%04x >' % ord(lval))
      for j in right[i]:
        lineout.append(' \u%04x' % ord(j))
      i += 1
      lineout.append(' ;')
      print ''.join(lineout)
  return True
  


# Run all the tests.
def main(argv=None):

  printMappingRules()
  

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
  