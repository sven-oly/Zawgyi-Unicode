#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

# Zawgyi font encoding conversion to Unicode form

Description = ZAWGYI_description = u'Zawgyi font encoding conversion'

TRANS_LIT_RULES = ZAWGYI_UNICODE_TRANSLITERATE = u"""# This transform converts Zawgyi "encoded" Burmese into proper
# unicode. Zawgyi is a popular encoding scheme in Myanmar. It uses
# the Myanmar unicode range but assigns different characters or
# glyphs to some codepoints. In addition to the character mapping,
# there is reordering of codepoints needed to match the expected
# unicode order. This reordering is context-based.
#
# This transform is done in two main stages:
# (1) Map all Zawgyi codepoints to their Unicode counterpart.
# (2) Perform reordering.

# Modern Burmese digits & Unicode code points.
$nondigits = [^\u1040-\u1049];
$consonant = [\u1000-\u1021];
$vowelsign = [\u102B-\u1030\u1032];  # Unicode vowel signs except E (1031)
$umedial = [\u103B-\u103E];    # Medial codepoints in Unicode
$vowelmedial = [\u102B-\u1030\u1032\u103B-\u103F];  # Union of vowel signs and medials
$ukinzi = \u1004\u103A\u1039;  # Codepoints representing kinzi in Unicode

# ZAWGYI MYANMAR CONSONANT SIGN MEDIAL RA
# This character has multiple representations in the Zawgyi font.
$zmedialra = [\u103B\u107E-\u1084];

$vowelsAndConsonants = [\u1000-\u102a];

####
#### STAGE 1: CODEPOINT MAPPING FROM ZAWGYI TO UNICODE
####

# Kinzi (predefined ligatures)
# Move base character to the right
($consonant) \u103A \u1064 → $ukinzi $1 \u103B;
($consonant) \u1064 → $ukinzi $1;
\u1064 → $ukinzi;

# Special cases moving base character to right before
($consonant) \u108b → $ukinzi $1 \u102D;
($consonant) \u108C → $ukinzi $1 \u102E;
($consonant) \u108D → $ukinzi $1 \u1036;

# Special cases moving Kinzi block to left
($consonant) \u103A \u1033 \u108B → $ukinzi $1 \u103B \u102D \u102F;
($consonant) \u103A \u108b → $ukinzi $1 \u103B \u102D ;
($consonant) \u103A \u108C \u1033 → $ukinzi $1 \u103B \u102E \u102F;
($consonant) \u103A \u108C → $ukinzi $1 \u103B \u102E ;
($consonant) \u103A \u108D → $ukinzi $1 \u103B \u1036 ;
($consonant) \u103A \u108e → $1 \u103B \u102D \u1036 ;

\u108B → $ukinzi \u102D ;
\u108C → $ukinzi \u102E ;
\u108D → $ukinzi \u1036 ;

# Consonants (only the ones that have to change)
\u106A ($vowelsign) \u1038 → \u1025 $1 \u1038 ;  # U sound
\u106A → \u1025 ;  # NYA
\u106B → \u100A ;
\u108F → \u1014 ;
\u1090 → \u101B ;
\u1086 → \u103F ;

# yapin
\u103A → \u103B ;
\u107D → \u103B ;

# wasway
\u103C \u108A → \u103D \u103E;  # To avoid duplicate medials
\u103C → \u103D ;
\u108A → \u103D \u103E ;

# hatoh
\u103D → \u103E ;
\u1087 → \u103E ;
\u1088 → \u103E \u102F ;
\u1089 → \u103E \u1030 ;

# asat
\u1039 → \u103A ;

# Vowels
\u1033 → \u102F ;
\u1034 → \u1030 ;
\u105A → \u102B \u103A ;
\u108E → \u102D \u1036 ;

# lDot
# Special cases to move dot to right of base consonant
\u1031 \u1094 ($consonant) \u103D → $1 \u103E \u1031 \u1037 ;
\u1094 → \u1037 ;
\u1095 → \u1037 ;

# Special cases for 1025 vs 1009
\u1025 \u1061 → \u1009 \u1039 \u1001;
\u1025 \u1062 → \u1009 \u1039 \u1002;
\u1025 \u1065 → \u1009 \u1039 \u1005;
\u1025 \u1068 → \u1009 \u1039 \u1007;
\u1025 \u1076 → \u1009 \u1039 \u1013;
\u1025 \u1078 → \u1009 \u1039 \u1015;
\u1025 \u107A → \u1009 \u1039 \u1017;
\u1025 \u1079 → \u1009 \u1039 \u1016;

($consonant) \u103A \u1039 → $1 \u103A \u103B;

# Stacked Consonants
\u1060 → \u1039 \u1000 ;
\u1061 → \u1039 \u1001 ;
\u1062 → \u1039 \u1002 ;
\u1063 → \u1039 \u1003 ;
\u1065 → \u1039 \u1005 ;
\u1066 → \u1039 \u1006 ;
\u1067 → \u1039 \u1006 ;
\u1068 → \u1039 \u1007 ;
\u1069 → \u1039 \u1008 ;
\u106C → \u1039 \u100B ;
\u106D → \u1039 \u100C ;
\u1070 → \u1039 \u100F ;
\u1071 → \u1039 \u1010 ;
\u1072 → \u1039 \u1010 ;
\u1096 → \u1039 \u1010 \u103D;
\u1073 → \u1039 \u1011 ;
\u1074 → \u1039 \u1011 ;
\u1075 → \u1039 \u1012 ;
\u1076 → \u1039 \u1013 ;
\u1077 → \u1039 \u1014 ;
\u1078 → \u1039 \u1015 ;
\u1079 → \u1039 \u1016 ;
\u107A → \u1039 \u1017 ;
\u107B → \u1039 \u1018 ;
\u1093 → \u1039 \u1018 ;
\u107C → \u1039 \u1019 ;
\u1085 → \u1039 \u101C ;

# Pre-defined ligatures
\u106E → \u100D\u1039\u100D ;
\u106F → \u100D\u1039\u100E ;
\u1091 → \u100F\u1039\u100D ;
\u1092 → \u100B\u1039\u100C ;
\u1097 → \u100B\u1039\u100B ;
\u104E → \u104E\u1004\u103A\u1038 ;

# yayit
($zmedialra)+ → \u103C ;

####
#### STAGE 1.1: Remove spaces immediately before combining characters.
####
::Null;

# Don't remove spaces before E vowel or medial Ra
([:WSpace:]) \u1037 > \u1037 $1;
([:WSpace:]+) ([\u102b-\u1030\u1032-\u103b\u103d\u103e]) → $2;

# Remove a duplicate
\u1037 \u1037+ → \u1037;

# Evowel before 0 only -> convert to the consonant.
\u1031 \u1040 ($nondigits) > \u1031 \u101D $1;

# Move e-vowel after medials
([\u1031]+) $ukinzi ($consonant) > $ukinzi $2 \u1031;
\u1031 \u103c ($consonant) > $1 \u103c \u1031;
\u1031 ($consonant) ($umedial+) > $1 $2 \u1031;
\u1031 ($vowelsAndConsonants) > $1 \u1031;

\u1031 (\u1037+) ($consonant) > $2 \u1031 \u1037 ;

\u1031 ($consonant) $ukinzi > $ukinzi \u1031 ;

####
#### STAGE 2: POST REORDERING RULES FOR UNICODE RENDERING
#### Now every codepoint is Unicode.  This starts conversion
#### from semi-visual order to logical order.
####
::Null;

# Case of MYANMAR digit being used instead of a letter
# Lone digit zero at start
^ \u1040 ($nondigits) → \u101D $1;

([\u102b-\u103f]) \u1040 ($nondigits) → $1 \u101d $2;
# Lone digit 4
^ \u1044 ($nondigits) → | \u104E $1 ;
([\u102b-\u103f]) \u1044 ($nondigits) → $1 \u104E $2;

# Simpler replacements for Zawgyi 1025
# TODO: REMOVE \u1025 \u103A → \u1025 \u103A;
\u1025 \u102E → \u1026;

# Asat and dot below reordering, to Unicode NFC.
\u103A\u1037 → \u1037\u103A;

# Reorder some vowel signs
\u1036 ($umedial*) ($vowelsign+) → $1 $2 \u1036 ;
([\u102B\u102C\u102F\u1030]) ([\u102D\u102E\u1032]) → $2 $1;

# Move ra medial, but not others.
\u103C ($consonant) → $1 \u103C;

# Replace CA + YA with JHA
\u1005\u103b → \u1008;

####
#### Stage 3
#### Move \u1031, \u1036, and \u103C after consonants.

::Null;

($umedial) \u1039 ($consonant) > \u1039 $2 $1;

\u103C \u103A \u1039 ($consonant) → \u103A \u1039 $1 \u103C;

\u1036 ($umedial+) → $1 \u1036;


####
#### Stage 4
#### Reordering medials, dot below, contractions, E sign, and asat.

::Null;

# Reorder the medials
([\u103C\u103D\u103E]+) \u103B → \u103B $1;
([\u103D\u103E]+) \u103C → \u103C $1;
\u103E\u103D → \u103D\u103E ;

# Contractions with vowel signs
([\u1031]+) ($vowelsign*) \u1039 ($consonant) → \u1039 $3 $1 $2;
($vowelsign+) \u1039 ($consonant) → \u1039 $2 $1;

# Move vowel sign E \u1031 after medials, but not across consonants
($umedial*) ([\u1031]+) ($umedial*) → $1 $3 $2;

# Reorder dot below after medials and vowel diacritics
\u1037 ([\u102D-\u1030\u1032\u1036]) → $1 \u1037;
\u1037 ($umedial+) → $1 \u1037;

# Move vowel signs after medials
($vowelsign+) ($umedial+) → $2 $1;

# Reorder modifiers and asat
($consonant) ([\u102B-\u1032\u1036\u103B-\u103E]) \u103A ($consonant) → $1 \u103A $2 $3;


####
#### Stage 5.  More reorderings
#### Vowel signs after medials, sort medials, 
####
::Null;

([\u1031]+) ($umedial+) → $2 $1;

# More moving vowel signs after medials
($vowelsign) ($umedial) → $2 $1;

# Sort the medials
([\u103C\u103D\u103E]) \u103B → \u103B $1;
([\u103D\u103E]) \u103C → \u103C $1;
\u103E\u103D → \u103D\u103E ;

# Move visarga (\u1038) after other signs
\u1038 ($vowelmedial) → $1 \u1038;
\u1038 ([\u1036\u1037\u103A]) → $1 \u1038;

# Reorder
\u1036 \u102f → \u102f \u1036;

###
### Stage 6
### Finish medial sorting, fix conflicting and extra diacritics
###

::Null;
# Fix duplicate combiners
\u102D \u102D+ → \u102D;
\u102E \u102E+ → \u102E;
\u102F \u102F+ → \u102F;
\u1030 \u1030+ → \u1030;
\u1032 \u1032+ → \u1032;
\u1033 \u1033+ → \u1033;
\u1035 \u1035+ → \u1035;
\u1036 \u1036+ → \u1036;
\u1037 \u1037+ → \u1037;
\u1039 \u1039+ → \u1039;
\u103a \u103a+ → \u103a;
\u103b \u103b+ → \u103b;
\u103c \u103c+ → \u103c;
\u103d \u103d+ → \u103d;
\u103e \u103e+ → \u103e; # http://unicode.org/cldr/trac/ticket/10386

# Fix overlapping signs
\u102F \u1030 → \u102F;
\u102F \u103A → \u102F;
\u102D \u102E → \u102E;

# Remove space directly before diacritics.
[:WSpace:]+ ([\u102b-\u1032\u1036-\u103e]) → $1;

# Fix 103B/103A order for asat.
($consonant) \u103B \u103A → $1 \u103A \u103B;
"""

date_entered = '25-June-2018'
description = 'Revised rules for Zawgyi to Unicode'

# Zawgyi and expected Unicode value.
# Do not forget to make each test string with 'u'.
TEST_DATA = [
    [0, u'ေခေဂေဃ', u'ခေဂေဃေ', 'adjacent consonants with evowels'],
    [1, u'ေ႔့့ခွ', u'ခှေ့', 'Lower dots with evowel'],
    [2, u'ေႂကၣ', u'က္ဃြေ', 'evowel, ra, subscript'],
    [3, u'ေျကၢိ့း', u'က္ဂြေိ့း', 'E + ra + subscript + vowels'],
]


def TestData():
  return TEST_DATA


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
