#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

# Zawgyi font encoding conversion to Unicode form

Description = ZAWGYI_description = u'UniMon font encoding conversion'

TRANS_LIT_RULES = ZAWGYI_UNICODE_TRANSLITERATE = u"""# Modern Burmese digits & Unicode code points.
$nondigits = [^\u1040-\u1049];
$space = '\u0020';
$consonant = [\u1000-\u1021];
$vowelsign = [\u102B-\u1030\u1032];
$umedial = [\u103B-\u103E];
$vowelmedial = [\u102B-\u1030\u1032\u103B-\u103F];
$ukinzi = \u1004\u103A\u1039;
$zmedialra = [\u103B\u107E-\u1084];
# #### STAGE (1): CODEPOINT MAPPING FROM ZAWGYI TO UNICODE
($consonant) \u103A \u1064 > $ukinzi $1 \u103B;
($consonant) \u1064 > $ukinzi $1;
\u1064 > $ukinzi;
($consonant) \u108b > $ukinzi $1 \u102D;
($consonant) \u108C > $ukinzi $1 \u102E;
($consonant) \u108D > $ukinzi $1 \u1036;
($consonant) \u103A \u1033 \u108B > $ukinzi $1 \u103B \u102D \u102F;
($consonant) \u103A \u108b > $ukinzi $1 \u103B \u102D ;
($consonant) \u103A \u108C \u1033 > $ukinzi $1 \u103B \u102E \u102F;
($consonant) \u103A \u108C > $ukinzi $1 \u103B \u102E ;
($consonant) \u103A \u108D > $ukinzi $1 \u103B \u1036 ;
($consonant) \u103A \u108e > $1 \u103B \u102D \u1036 ;
\u108B > $ukinzi \u102D ;
\u108C > $ukinzi \u102E ;
\u108D > $ukinzi \u1036 ;
\u106A ($vowelsign) \u1038 > \u1025 $1 \u1038 ;
\u106A > \u1009 ;
\u106B > \u100A ;

# Ignore inserted invisible spaces
\u200b > ;

$zmedialra > \u103c;

\u108F > \u1014 ;
\u1090 > \u101B ;
\u1086 > \u103F ;
\u103A > \u103B ;  # Rule 21
\u103B > \u103C ;  # Rule 21
\u107D > \u103B ;
\u103C \u108A > \u103D \u103E;
\u103C > \u103D ;  # Rule 24
\u108A > \u103D \u103E ;
\u103D > \u103E ;   # Rule 26
\u1087 > \u103E ;
\u1088 > \u103E \u102F ;
\u1089 > \u103E \u1030 ;
\u1039 > \u103A ;  # Rule 30
\u1033 > \u102F ;
\u1034 > \u1030 ;
\u105A > \u102B \u103A ;
\u108E > \u102D \u1036 ;
\u1031 \u1094 ($consonant) \u103D > $1 \u103E \u1031 \u1037 ;
\u1094 > \u1037 ;
\u1095 > \u1037 ;
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

date_entered = '18-July-2015'
description = 'First try for transliteration rules for Zawgyi to Unicode'

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