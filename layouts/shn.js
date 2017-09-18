/ Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS-IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// TODO: Reference

var SHN_LAYOUT = {
  'id': 'Shan',
  'title': 'Shan',
  'mappings': {
    '': {
      '': '\u1050\u1041\u1042\u1043\u1044\u1045\u1046\u1047\u1048\u1049' +
            '\u1040-=' +
          '\u1078\u1010\u107c\u1019\u1022\u1015\u1075\u1004\u101d\u1081' +
            '[]\\' +
          '\u1031\u1084\u102d\u103a\u103d\u1089\u1087\u102f\u1030' +
            '\u1088\'' +
          '\u107d\u1011\u1076\u101C\u101a\u107a\u1062,./'
    },
    'c': {
      '': '~\u1050\u1041\u1042\u1043\u1044\u1045\u1046\u1047\u1048\u1049-=',
      'q': '\u1078\uaa66',
      'o': '\ua9e1',
      's': '\ua9e6',
      'z': '\ua938\uaa67'
    },
    's': {
      '': '!@#$%^&*()_+' +
          '\\uaa61\u107b\ua9e3\u10ae\u1053\u103c\u107f\u1077\u1004\u101d' +
              '[]\\' +
          '\u1035\u1085\u102e\u1082\u1082\u103f\u1086\u201d\u108a\u1038\u201c' +
          '{{}}\uaaba\ua9e0\uaabe\u103b\u109f\u1083\u104A\u104B?'
    },
    'c': { // One key for Kinzi.
      '1': '\u1091\u1092\u1093\u1094\u1095\u1096\u1097\u1098\u1099',
      'w': '\uaa68',
      'o': '\ua9e2',
      'x': '\uaa69'
    },
    'l,cl': {
      '': '`1234567890-=' +
          'qwertyuiop[]\\' +
          'asdfghjkl;\'' +
          'zxcvbnm,./'
    },
    'sl,scl': {
      '': '~!@#$%^&*()_+' +
          'QWERTYUIOP{}|' +
          'ASDFGHJKL:"' +
          'ZXCVBNM<>?'
    }
  },
  'transform' : {
    // Reorder vowel E after consonant
    '\u200c\u1031([\u1000-\u102a\u103f\u104e])': '$1\u1031',

    // Keep E after medials
    '([\u103c-\u103e]*\u1031)\u001d\u103b': '\u103b$1',
    '([\u103b]*)([\u103d-\u103e]*)\u1031\u001d\u103c': '$1\u103c$2\u1031',
    '([\u103b\u103c]*)([\u103e]*)\u1031\u001d\u103d': '$1\u103d$2\u1031',
    '([\u103b-\u103d]*)\u1031\u001d\u103e': '$1\u103e\u1031',

    // Reorder medials without E vowel
    '([\u103c-\u103e]+)\u001d?\u103b': '\u103b$1',
    '([\u103b]*)([\u103d-\u103e]+)\u001d?\u103c': '$1\u103c$2',
    '([\u103b\u103c]*)([\u103e]+)\u001d?\u103d': '$1\u103d$2',

    // Move E after kinzi in steps.
    '\u1004\u1031\u001d\u103a': '\u1004\u103a\u1031',
    '\u1004\u103a\u1031\u001d\u1039': '\u1004\u103a\u1039\u1031',
    '\u1004\u103a\u1039\u1031\u001d([\u1000-\u102a\u103f\u104e])':
    '\u1004\u103a\u1039$1\u1031',

    // Move E after subscripted consonant in two steps.
    '([\u1000-\u102a\u103f\u104e])\u1031\u001d\u1039': '$1\u1039\u1031',
    '\u1039\u1031\u001d([\u1000-\u1019\u101c\u101e\u1020\u1021])' :
    '\u1039$1\u1031',

    // Move vowel anusvara relative to vowel signs
    '\u1036([\u102d|\u102e\u1030|\u102f|\u1030])': '$1\u1036',

    // Move vowel anusvara relative to medials signs
    '\u1036([\u103b|\u103c\u103d|\u103e])': '$1\u1036'
  }

};

// Load the layout and inform the keyboard to switch layout if necessary.
google.elements.keyboard.loadme(SHN_LAYOUT);
                                                                                
