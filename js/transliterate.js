// Functions implementing a subset of ICU transliterator, much like the Python version.


// ruleList is a list of 2-element lists, with [pattern, subst]
function applyPhase(instring, ruleList, debug) {

  var start = 0;
  var limit = instring.length;
  var currentString = instring;

  while start < limit {
    var ruleIndex = 0;
    var matchObj = null;
    limit = currentString.length;

    for (rule in ruleList) {
      var pattern = rule[0];
      var subst = rule[1];

      // TODO(ccornelius): Check if this can be initialized in the outer look,
      // and reset only when a chance is made.
      var strToMatch = currentString.substring(start);
      var matchObj = strToMatch.match(pattern);

      if (matchObj) {
	// replace the parts and compute a new limit.
	// reset the current string.
      }

    }
  }
}
