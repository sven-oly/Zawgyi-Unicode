#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re

# Regular expression for Zawgi detection.
# Note that this is too sensitive, finding typos and common mistakes in
# otherwise Unicode-compliant strings.
isZawgyiRegEx = (
    # REMOVED THIS TO AVOID LABELING OTHER LANGUAGES AS ZAWGYI
    # [\u105a\u1060-\u1097]|"  # Zawgyi characters outside Unicode range
    "[\u1033\u1034]|"  # These are Mon characters
    "\u1031\u108f|"
    "\u1031[\u103b-\u103e]|"  # Medial right after \u1031
    "[\u102b-\u1030\u1032]\u1031|"  # Vowel sign right after before \u1031
    " \u1031| \u103b|"  # Unexpected characters after a space
    "^\u1031|^\u103b|\u1038\u103b|\u1038\u1031|"
    "[\u102d\u102e\u1032]\u103b|\u1039[^\u1000-\u1021]|\u1039$"
    "|\u1004\u1039[\u1001-\u102a\u103f\u104e]"  # Missing ASAT in Kinzi
    "|\u1039[^u1000-\u102a\u103f\u104e]"  # 1039 not before a consonant
    # Out of order medials
    "|\u103c\u103b|\u103d\u103b"
    "|\u103e\u103b|\u103d\u103c"
    "|\u103e\u103c|\u103e\u103d"
    # Bad medial combos. Actually a strong indicator of double converted strings.
    "|\u103b\u103c"
    # Out of order vowel signs
    "|[\u102f\u1030\u102b\u102c][\u102d\u102e\u1032]"
    "|[\u102b\u102c][\u102f\u102c]"

    # Second 1039 with bad followers
    "|[\u1000-\u102a\u103f\u104e]\u1039[\u101a\u101b\u101d\u101f\u1022-\u103f]"
    # Other bad combos.
    "|\u103a\u103e"
    "|\u1036\u102b]"
    # multiple upper vowels
    "|\u102d[\u102e\u1032]|\u102e[\u102d\u1032]|\u1032[\u102d\u102e]"
    # Multiple lower vowels
    "|\u102f\u1030|\u1030\u102f"
    # Multiple A vowels
    "|\u102b\u102c|\u102c\u102b"
    # Shan digits with vowels or medials or other signs
    "|[\u1090-\u1099][\u102b-\u1030\u1032\u1037\u103a-\u103e]"

    # Isolated Shan digit
    "|[\u1000-\u10f4][\u1090-\u1099][\u1000-\u104f]"  # Maybe too inclusive
    "|^[\u1090-\u1099][\u1000-\u102a\u103f\u104e\u104a\u104b]"
    "|[\u1000-\u104f][\u1090-\u1099]$"
    # Diacritics with non-Burmese vowel signs
    "|[\u105e-\u1060\u1062-\u1064\u1067-\u106d\u1071-\u1074\u1082-\u108d"
    "\u108f\u109a-\u109d]"
    "[\u102b-\u103e]"

    # Consonant 103a + some vowel signs
    "|[\u1000-\u102a]\u103a[\u102d\u102e\u1032]"
    # 1031 after other vowel signs
    "|[\u102b-\u1030\u1032\u1036-\u1038\u103a]\u1031"

    # Using Shan combining characters with other languages.
    "|[\u1087-\u108d][\u106e-\u1070\u1072-\u1074]"

    # Non-Burmese diacritics at start, following space, or following sections
    "|^[\u105e-\u1060\u1062-\u1064\u1067-\u106d\u1071-\u1074"
    "\u1082-\u108d\u108f\u109a-\u109d]"
    "|[\u0020\u104a\u104b][\u105e-\u1060\u1062-\u1064\u1067-\u106d"
    "\u1071-\u1074\u1082-\u108d\u108f\u109a-\u109d]"

    # Wrong order with 1036
    "|[\u1036\u103a][\u102d-\u1030\u1032]"

    # Odd stacking
    "|[\u1025\u100a]\u1039"

    # More mixing of non-Burmese languages
    "|[\u108e-\u108f][\u1050-\u108d]"

    # Bad diacritic combos.
    "|\u102d-\u1030\u1032\u1036-\u1037]\u1039]"

    # Dot before subscripted consonant
    "|[\u1000-\u102a\u103f\u104e]\u1037\u1039"

    # Odd subscript + vowel signs
    "|[\u1000-\u102a\u103f\u104e]\u102c\u1039[\u1000-\u102a\u103f\u104e]"

    # Medials after vowels
    "|[\u102b-\u1030\u1032][\u103b-\u103e]"

    # Medials
    "|\u1032[\u103b-\u103e]"
    # Medial with 101b
    "|\u101b\u103c"

    # Stacking too deeply: consonant 1039 consonant 1039 consonant
    "|[\u1000-\u102a\u103f\u104e]\u1039[\u1000-\u102a\u103f\u104e]\u1039"
    "[\u1000-\u102a\u103f\u104e]"

    # Stacking pattern consonant 1039 consonant 103a other vowel signs
    # ****
    "|[\u1000-\u102a\u103f\u104e]\u1039[\u1000-\u102a\u103f\u104e]"
    "[\u102b\u1032\u103d]"

    # Odd stacking over u1021, u1019, and u1000
    "|[\u1000\u1005\u100f\u1010\u1012\u1014\u1015\u1019\u101a]\u1039\u1021"
    "|[\u1000\u1010]\u1039\u1019"
    "|\u1004\u1039\u1000"
    "|\u1015\u1039[\u101a\u101e]"
    "|\u1000\u1039\u1001\u1036"
    "|\u1039\u1011\u1032"

    # Vowel signs
    "|\u1037\u1032"
    "|\u1036\u103b"
)

# A start on typical typos in 
UNICODE_TYPO_PATTERNS = ("^\u1031[\u1001-\u1020]"  # vowelE at start
                         "|\\0020\u1031[\u1001-\u1020]"  # or after a space
                         "|^\u103c[\u1001-\u1020]"   # ra at start 
                         "|\u0020\u103c[\u1001-\u1020]"   # ra after space 
                         )
                         
# Patterns to clean up
CLEAN_UP_PATTERNS = (  # Digit before diacritic
  "|[\u1040-\u1049][\u102b-\u103e\u102b-\u1030\u1032\u1036\u1037\u1038\u103a]"
  # Single digit 0, 7 at start
  "|^[\u1040\u1047][^\u1040-\u1049]"
  )

# From shake-n-break.js
IS_ZAWGYI = ("[\u1050-\u109f]|\u0020[\u103b\u107e-\u1084]|"
                "\u0020\u1031|^\u1031|^\u103b|\u1038\u103b|\u1038\u1031|"
                "\u1033|\u1034|[\u102d\u102e\u1032]\u103b|"
                "\u1039[^\u1000-\u1021]|\u1039$|\u108c")
IS_UNICODE_MY = ("[ဃငစဆဇဈဉညတဋဌဍဎဏဒဓနဘရဝဟဠအ]်|ျ[က-အ]ါ|ျ[ါ-း]|"
                 "\u103e|\u103f|"
                 "\u1031[^\u1000-\u1021\u103b\u106a\u106b\u107e-\u1084\u108f\u1090]|"
                 "\u1031$|\u100b\u1039|\u1031[က-အ]\u1032|\u1025\u102f|\u103c\u103d")

# From observation of the characters in each font.
IN_MYAZEDI_NOT_Z = ("[\u1035\u1050-\u1059\u105d-\u105f\u1098-\u109f]|"
                    "\u107E[\u1001\u1002\u1004\u1005\u1007\u1008\u1012-\u1017]|"
                    # And more...
                    # Narrow consonants with wide Ra
                    ) 
reInMayzediNotZ = IN_MYAZEDI_NOT_Z.decode('unicode-escape')
 
IN_ZAWGYI_NOT_M = ("[u102b\u103a-\u103d\u105a]")
reInZawgyiiNotM = IN_ZAWGYI_NOT_M.decode('unicode-escape')

reZawgyiShake = IS_ZAWGYI.decode('unicode-escape')
reZawgyiShakeCompiled = re.compile(reZawgyiShake)
reUnicodeShake = IS_UNICODE_MY.decode('unicode-escape')
reUnicodeShakeCompiled = re.compile(reUnicodeShake)

zRE = isZawgyiRegEx.decode('unicode-escape')
zREC = re.compile(zRE)


# Detects if source text is Zawgyi, Unicode, or (eventually) Myazedi encoding.
def isZawgyiShake(textIn):
  # TODO: Finish
  matches = re.search(reZawgyiShakeCompiled, textIn, flags=0)
  if matches:
    return True
  else:
    return False


def isUnicodeShake(textIn):
  # TODO: Finish
  matches = re.search(reUnicodeShakeCompiled, textIn, flags=0)
  if matches:
    return True
  else:
    return False

    
def isZawgyi(textIn):
  # TODO: Finish
  matches = re.search(zRE, textIn, flags=0)
  if matches:
    return True
  else:
    return False


def isUnicode(textIn):
  # TODO: Finish
  matches = re.search(zRE, textIn, flags=0)
  if matches:
    return False
  else:
    return True  

    
def isMyazedi(textIn):
  # TODO: define algorithm
  if not isZawgyiShake(textIn):
    return False
    
  matchesM = re.search(reInMayzediNotZ, textIn, flags=0)
  matchesZ = re.search(reInZawgyiiNotM, textIn, flags=0)
  
  if matchesM and not matchesZ:
    return True
  else:
    return False
  return 'undefined'
