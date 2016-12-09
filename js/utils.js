// Utilities for handling text.

  // Takes hex text and converts to characters, displaying in another field.
function convertToText(inId, outId) {
  var textinput = document.getElementById(inId);
  var textoutput = document.getElementById(outId);
  var inChars = textinput.value;
  var outCharacters = uhexToChars(inChars)
  textoutput.innerHTML = outCharacters;
}

function  uhexToChars(textinput) {
  // blanks delimit
  var removed_uslash = textinput.replace(/\\u/g, " ");
  var hexSplit = removed_uslash.split(" ");
  // var hexSplit = textinput.split(" ");
  var charsOut = "";
  for (i = 0; i < hexSplit.length; i++) {
    var hex = hexSplit[i].replace("U+", "").trim();
    var charCode = parseInt(hex, 16);
    var newString = getUnicodeCharacter(charCode);
    charsOut += newString;
  }
  size = textinput.length
  return charsOut;
}

function charsToHexString(text) {
  var nums = "";
  for (i = 0; i < text.length; i++) {
    v = text.charCodeAt(i);
    var xout = v.toString(16)
    nums = nums + xout + " ";
  }
  return nums;
}

// From http://stackoverflow.com/questions/7126384/expressing-utf-16-unicode-characters-in-javascript
function getUnicodeCharacter(cp) {

    if (cp >= 0 && cp <= 0xD7FF || cp >= 0xE000 && cp <= 0xFFFF) {
        return String.fromCharCode(cp);
    } else if (cp >= 0x10000 && cp <= 0x10FFFF) {

        // we substract 0x10000 from cp to get a 20-bits number
        // in the range 0..0xFFFF
        cp -= 0x10000;

        // we add 0xD800 to the number formed by the first 10 bits
        // to give the first byte
        var first = ((0xffc00 & cp) >> 10) + 0xD800;

        // we add 0xDC00 to the number formed by the low 10 bits
        // to give the second byte
        var second = (0x3ff & cp) + 0xDC00;

        return String.fromCharCode(first) + String.fromCharCode(second);
    }
}
