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

// Myanmar3 layout: http://www.myanmarlanguage.org/unicode/myanmar3-keyboard-layout

var KSW_LAYOUT = {
  'id': 'ksw',
  'title': 'S\'gaw Karen',
  'mappings': {
    ',c': {
      '': '`1234567890-=' +
          '\u1006\u1001\u1014\u1019\u1021\u101a\u1000\u101c\u101E\u1005' +
            '\u101F:\\' +
          '\u1037\u1036\u1062\u102e\u102d\u1015{{\u103C\u1063}}\u1064' +
            '\u106d\u1038\u0012' +
          '\u1004\u1011\u1001\u1018\u1003\u1016{{\u103C\u102c}},.-'
    's,sc': {
      '': '~!@#$%^&*()_+' +
          '\u1030\u00a3\u20a0\u0e3f{}\u101b\u1002\u101d' +
          '\u1061\u1027/|' +
          '\u103c\u103E\u103b\u1060\u103D\u103a\u1032\u102f\u1030\u102b\"' +
          '\u1007\<>[]\u101a_\'\u2022?' +
          ''\u202b'
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
google.elements.keyboard.loadme(KSW_LAYOUT);
                                                                                
