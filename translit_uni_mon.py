#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import transliterate

# Mon 2010 & Unimon (maybe)

# Modern Burmese digits & Unicode code points.
# UniMon is mostly Zawgyi, but some differences.
Description = UNIMON_description = u'Mon 2010 / UniMon conversion'
TRANS_LIT_RULES = UNIMON_UNICODE_TRANSLITERATE = u"""#
$nondigits = [^\u1040-\u1049];
$space = '\u0020';
$consonant = [\u1000-\u1021];
$vowelsign = [\u102B-\u1030\u1032];
$umedial = [\u103B-\u103E];
$vowelmedial = [\u102B-\u1030\u1032\u103B-\u103F];
$ukinzi = \u1004\u103A\u1039;
$zmedialra = [\u103B\u107E-\u1083];
# #### STAGE (1): CODEPOINT MAPPING FROM ZAWGYI TO UNICODE
($consonant) \u103A \u1064 > $ukinzi $1 \u103B;
($consonant) \u1064 > $ukinzi $1;
\u1064 > $ukinzi;

\u106A ($vowelsign) \u1038 > \u1025 $1 \u1038 ;
\u106A > \u1009 ;
\u106B > \u100A ;

# Ignore inserted invisible spaces
\u200b > ;

# UniMon specific conversions
\u1022 > \u1007 \u103b \u103e ;
\u1026 > \u102d \u1032 ;
\u1028 > \u1000 \u1031 \u102f \u1036 \u102c ;
\u1033 > \u102f ;
\u1034 > \u1030 ;
\u1035 > \u1032 \u102b ;
\u1039 > \u103a ;
\u103a > \u103b ;
\u103b > \u103c ;
\u103c > \u103d ;
\u103d > \u103e ;
\u103e > \u1033 ;
\u103f > \u1015 \u1039 \u100d \u1032 ;

\u102a > \u1035 ;
\u103e > \u105e ;
\u103f > \u105f ;
\u1050 > \u1039 \u1021 ;
($consonant) \u1051 > $ukinzi $1 \u1033 ;
\u1052 > \u1039 \u101e ;
\u1053 > \u1039 \u1021 ;
\u1054 > \u1039 \u100a ;
\u1055 > \u1039 \u100e ;
\u1056 > \u1036 \u102b ;
($consonant) \u1057 > $ukinzi $1 \u102b ;

\u105b > \u1039 \u101b ;
\u105c > \u1060 ;
\u105d > \u1039 \u101e ;
\u105e > \u1039 \u105c ;
\u105f > \u1030 \u1021;
# \u1059;  Maybe unmapped?

$zmedialra > \u103c;

\u103A > \u103B ;  # Rule 21
\u103B > \u103C ;  # Rule 21
\u107D > \u103B ;
\u103C > \u103D ;  # Rule 24
\u103D > \u103E ;   # Rule 26
\u1087 > \u103E ;
\u1039 > \u103A ;  # Rule 30
\u1033 > \u102F ;
\u1034 > \u1030 ;
\u105A > \u102B \u103A ;
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
\u1070 > \u1039 \u100F ;
\u1071 > \u1039 \u1010 ;
\u1072 > \u1039 \u1010 ;
\u1073 > \u1039 \u1011 ;
\u1074 > \u1039 \u1011 ;
\u1075 > \u1039 \u1012 ;
\u1076 > \u1039 \u1013 ;
\u1077 > \u1039 \u1014 ;
\u1078 > \u1039 \u1015 ;
\u1079 > \u1039 \u1016 ;
\u107A > \u1039 \u1017 ;
\u107B > \u1039 \u1018 ;
\u107C > \u1039 \u1019 ;
\u106E > \u100D\u1039\u100D ;
\u106F > \u100D\u1039\u100E ;
\u104E > \u104E\u1004\u103A\u1038 ;
##### STAGE (2): POST REORDERING RULES FOR UNICODE RENDERING
::Null;
\u1044 \u103a > | \u104E \u103A ;
($nondigits) \u1040 ([\u102B-\u103F]) > $1 \u101D $2;
\u1031 \u1040 ($nondigits) > \u1031 \u101D $1;
\u1025 \u103A > \u1009 \u103A;
\u1025 \u102E > \u1026;
\u1037\u103A > \u103A\u1037;
\u1036 ($umedial*) ($vowelsign+) > $1 $2 \u1036 ;
([\u102B\u102C\u102F\u1030]) ([\u102D\u102E\u1032]) > $2 $1;
\u103C ($consonant) > $1 \u103C;
##### Stage 3
::Null;
([\u1031]+) $ukinzi ($consonant) > $ukinzi $2 \u1031;
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
([\u1031]+) ($vowelsign*) \u1039 ($consonant) > \u1039 $3 $1 $2;
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

date_entered = '16-June-2016'
description = 'First try for transliteration rules for UniMon to Unicode'

def printRules():
  print 'Rules for %s' % Description
  lines = TRANS_LIT_RULES.split('\n')
  ruleNum = 0
  for line in lines:
    line = line.strip()
    if len(line) > 0 and line[0] != '#':
      print ('%4d\t%s' % (ruleNum, line))
      ruleNum += 1

def main(argv=None):
  printRules()


if __name__ == "__main__":
    print 'ARGS = %s' % sys.argv 
    sys.exit(main(sys.argv))