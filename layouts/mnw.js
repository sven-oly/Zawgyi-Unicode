// Licensed under the Apache License, Version 2.0 (the "License");
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

var MNW_LAYOUT = {
  'id': 'mnw',
  'title': 'Mon (in progress)',
  'mappings': {
    ',c': {
      '': '?\u1041\u1042\u1043\u1044\u1045\u1046\u1047\u1048\u1049\u1040{{}}-' +
       '\u101b\u1010\u1014\u1019\u1021\u1015\u1000\u1004\u1010\u1005' +
       '\u1028\u103e\u102e\u1033\u103d\u1037\u1034\u105e' +
            '\u1027\u105d\u104f' +
      '{{\u1007\u103b\u103e}}\u1012\u1002\u101c\u1017\u100a\u102c\u101a\u1038\u101d'
    },
    's,sc': {
      '': '\u104E\u103f\u100c\u100B\u1026\u104c\u104d{{}}()_+' +
          '\u1025\u1011\u1023\u1008\u1035\u1016\u1001{{\u1004\u1082}}\u1051\u1006' +
          '\u1027\u105d\u1028' +
          '\u1017\u103E\u102E\u1039\u103D\u1036\u1032\u1012\u1013\u1002\u0022' +
       '\u1007\u1012\u1003\u1020\u1018\u1009\u102f\u1050\u1038\u104a'
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
google.elements.keyboard.loadme(MNW_LAYOUT);
                                                                                
