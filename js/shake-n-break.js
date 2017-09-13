// From http://www.novasteps.com/shake-n-break.js
var consonants;
var zg_consonants;
var common_vowels;
var mm_vowels;
var zg_vowels;
var medials;
var zg_medials;
function zg_break(){
}
function mm_break(){
}
var IS_MYANMAR_RANGE = "[က-အ]+|[\u1025-\u1027]";
var IS_UNICODE_MY = "[ဃငစဆဇဈဉညတဋဌဍဎဏဒဓနဘရဝဟဠအ]်|ျ[က-အ]ါ|ျ[ါ-း]|\u103e|\u103f|\u1031[^\u1000-\u1021\u103b\u106a\u106b\u107e-\u1084\u108f\u1090]|\u1031$|\u100b\u1039|\u1031[က-အ]\u1032|\u1025\u102f|\u103c\u103d";
var IS_ZAWGYI = "[\u1050-\u109f]|\u0020[\u103b\u107e-\u1084]|\u0020\u1031|^\u1031|^\u103b|\u1038\u103b|\u1038\u1031|\u1033|\u1034|" + // [\u102d\u102e\u1032]\u103b|
    "\u103a\u102c|" +
    "\u1039[^\u1000-\u1021]|\u1039$|\u108c";
var reMyanmar = [new RegExp(IS_MYANMAR_RANGE)];
var reUnicode_my = [new RegExp(IS_UNICODE_MY)];
var reZawgyi = [new RegExp(IS_ZAWGYI)];

function is_myanmar (input) {
	for(var i=0; i<reMyanmar.length; i++){
		if(reMyanmar[i].test(input.value)) return true;
	}
	return false;
}

function is_unicode_my(input) {
	for(var i=0; i<reUnicode_my.length; i++){
		if(reUnicode_my[i].test(input.value)) return true;
	}
	return false;
}

function is_zawgyi(input){
	for(var i=0; i<reZawgyi.length; i++){
		if(reZawgyi[i].test(input.value)) return true;
	}
    return false;
}

function check_encoding() {
	var result = document.getElementById("result");
	var input = document.getElementById("input");
	result.innerHTML = "Not Detected.";
	if (!is_myanmar(input)){
		result.innerHTML = "Myanmar Range [က-အ] not present in text";
	}
	if (is_zawgyi(input)){
		result.innerHTML = "Zawgyi";
		input.style.fontFamily = "Zawgyi-One, Zawgyi1";
	}
	if (is_unicode_my(input)){
		result.innerHTML = "Unicode";

	    if (isMalformedUnicode(input)) {
		  result.innerHTML = "Unicode with typographic errors";
		}
		input.style.fontFamily = "Padauk, Myanmar3, Parabaik, 'MyMyanmar Unicode', Myanmar2";
	}
}

// Myazedi detection, based on simple observations.
// 28-Apr-2015 (CWC)

var IN_MYAZEDI_NOT_Z = "[\u1035\u1050-\u1059\u105d-\u105f\u1098-\u109f]|" +
                    "\u107E[\u1001\u1002\u1004\u1005\u1007\u1008\u1012-\u1017]";
                    // Maybe need to complete narrow consonants
var reInMayzediNotZ = [new RegExp(IN_MYAZEDI_NOT_Z)];
 
var IN_ZAWGYI_NOT_M = ("[u102b\u103a-\u103d\u105a]");
var reInZawgyiiNotM = [new RegExp(IN_ZAWGYI_NOT_M)];

function is_myzaedi(input) {
	for(var i=0; i<reInZawgyiiNotM.length; i++){
		if(reInZawgyiiNotM[i].test(input.value)) return false;
	}
    
    for(var i=0; i<reInMayzediNotZ.length; i++){
		if(reInMayzediNotZ[i].test(input.value)) return true;
	}
    return false;
}

/* Code to detect and fix malformed Unicode - not comprehensive but handles almost all
   common problems.

  Left to fix: ြေဗာင်းြဗန် (ကြိဝိ). The medial ra (103c) and vowelE (1031) need to move right.
    (103c 1031 1017 102c 1004 103a 1038 103c 1017 1014 103a 20 28 1000 103c 102d 101d 102d 29 )

  CWC, 13-May-2015.
*/

// Common patterns in malformed Burmese text in Unicode.
function testMalformed() {
  var test1 = "အကေြာင်း (ဝိ)";
  return isMalformedUnicode(test1);
}
   
// TODO: Make sure that this is correct
function tryFix(inString) {
  
  if (inString.map) {
     return inString.map(tryFix);
  }
  // For each matching pattern in unicodeFixes, apply pattern until no more matches are found.
  var outString = inString;
  var rules = "";
  for (var i=0; i < unicodeFixes.length; i++) {
    try {
      pattern = new RegExp(unicodeFixes[i][0]);
    }
    catch (e) {
      return unicodeFixes[i][0];
    }
    if (pattern.test(inString)) {
      var newString = outString;
      do {
        // Try applying the replacement.
        outString = newString;
        newString = outString.replace(pattern, unicodeFixes[i][1]);
        rules += i + " ";
      } while (newString != outString);
    }
  }
  return outString;  // DEBUGGING + " : " + rules;
}

// Common patterns in malformed Burmese text in Unicode.

var unicodeMalformations = "\u1031[\u103a-\u103e]|^\u103c|[\u102b-\u102f\u1032\u1036-\u1038][\u103b-\u103e]|" + // Bad sign ordering
   "[\u1037\u1038]\u1036|\u1036\u102f|\u102f[\u102d\u102e\u1032]|[$\u0029]\u1031|" + 
   "\u102d\u103a" +
     "\u102d\u102d|\u103a\u103a|\u103e\u103b|\u103e\u103d|\u103d\u103b|" + // Duplicate signs
   "\u1004\u1031\u103a\u1039|" +  // vowelE inserted into Kinzi sequence
   "\u102c\u1039"; // Subscripting errors
   // ?? Isolated signs, e.g., \u102e
var isUMalformed = new RegExp(unicodeMalformations);

function isMalformedUnicode(input) {
  if (input.map) {
     return input.map(isMalformedUnicode);
  }
  else {
    // A single value
    if (isUMalformed.test(input)) {
      return "bad Unicode";
    }
    else {
    return "OK";
    }
  }
}


// ?? For each malformed Unicode, can we provide a rule to fix, e.g., "\u1031([\u103a-\u103e])" --> "$1\u1031".
// These rules may need to be applied more than once to move some characters over several positions.
var unicodeFixes = [
  ["\u1004\u1031\u103a\u1039([\u1000-\u1021])",
   "\u1004\u103a\u1039$1\u1031"],  // vowelE inserted into Kinzi sequence
  ["\u1031([\u103a-\u103e])", "$1\u1031"],
  ["^\u103c([\u1000-\u1021])", "$1\u103c"],
  ["([\u102b-\u102f\u1032\u1036-\u1038])([\u103b-\u103e])", "$2$1"],
  ["([\u1037\u1038])\u1036", "\u1036$1"],
   ["\u1036([\u102b-\u1030\u1032\u103b-\u103e]+)", "$1\u1036"],
   ["\u102f([\u102d\u102e\u1032])", "$1\u102f"],
   ["\u102d\u102b", "\u102b\u102d"],
   ["\u102d(\u102d+)", "\u102d"],
   ["\u103a(\u103a+)", "\u103a"],
   ["\u103e\u103b", "\u103b\u103e"],
   ["\u103e\u103d", "\u103d\u103e"],
   ["\u103d\u103b", "\u103b\u103d"],
   ["\u1032([\u103a-\u103e])", "$1\u1032"],
   ["\u102c\u1039([\u1000-\u1021])", "\u1039$1\u102c"],
   ["\u102d\u103a", "\u102d"],  // ??? Remove the asat because the vowel sign overwrites it?
   [/\)\u1031/, /\u1031\)/],
   ];
