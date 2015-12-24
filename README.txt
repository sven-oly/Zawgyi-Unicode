Initial release 25-April-2015, Craig Cornelius

References for Myanmar text and converts.
Unicode:
  http://unicode.org/notes/tn11/UTN11_3.pdf

Detector:
  http://www.novasteps.com/shake-n-break.html
  http://www.novasteps.com/shake-n-break.js

A listing of some Burmese non_unicode fonts:
  http://www.wazu.jp/gallery/Fonts_Myanmar.html
  
  http://mmunicodefonts.blogspot.com/
  
  Myazedi font source
  http://www.myazedi.com/mmfonts/v2/
  Sample text: မေစတီ ယူနီကုဒ္ (Unicode) စာ႟ုိက္စနစ္ အဆင့္ဴမၟင့္
  Layout:
    http://www.myazedi.com/mmfonts/v2/Font%20Printout%20V2.pdf
    
Font converters: http://burglish.my-mm.org/latest/trunk/web/fontconv.htm

Converter source:
  https://github.com/greenlikeorange/knayi-myscript/blob/master/README.md
  
Parses syllables:
  https://github.com/thanlwinsoft/MyanmarParser
  
  
API:

Put string to display from URL:

http://zawgyi-unicode-test.appspot.com/?text=

Get JSON results from detectors.
http://zawgyi-unicode-test.appspot.com/detect/?text=ဘယ္

Returns
  {"isZ": true, "isU": false, "isUShake": false, "isZShake": true, 
   "input": "\u1018\u101a\u1039", "errmsg": "OK"}
   
Notes: Myazedi test is not yet developed.