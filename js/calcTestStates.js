// Javascript tests of support calculator functions.

var numSuccess = 0;
var numFailure = 0;
var failureList = {};

function clearTests() {
  numSuccess = 0;
  numFailure = 0;
  failureList = {};
}


function runAllCalStateTests() {
  testAdd1();
  testAdd2();
}

function testAdd1() {
  clearTests();
  doOperator('clear X');
  doOperator('clear A');
  verifyValue(getX(), 0, 'Cleared x');
  verifyValue(getX(), 0, 'Cleared x');
  
  // Simple 74 + 7 =
  numberClick(70);
  numberClick(4);
  // Check that X has 74.
  
  verifyValue(getX(), 74, 'Enter 74');
  doOperator('+');
  // Check state
	
  numberClick(7);
  // Check X and accum
  verifyValue(getX(), 7, 'Enter 7');
	
  doOperator('=');
  verifyValue(getX(), 81, '= 81');
	
  var tempOut = document.getElementById('test_output');
  var outLine = 'testAdd1: ' + numSuccess + ' pass, ' +  numFailure + ' fail. Failures = ' +
    failureList;
  tempOut.innerHTML = outLine;
  tempOut.value = outLine; 
}

function testAdd2() {
  clearTests();
  doOperator('clear X');
  doOperator('clear A');
  // Simple 74 + 7 - 3 * 2 =
  clearTests();
  numberClick(70);
  numberClick(4);

  // Check that X has 74.
  verifyValue(getX(), 74, 'Enter 74');
	
  doOperator('+');
  // Check state
  verifyValue(getAccum(), 74, 'Accum = 74');
	
  numberClick(7);
  // Check X and accum
  verifyValue(getX(), 74, 'X = 7');
  verifyValue(getAccum(), 74, 'Accum = 74');
	
  doOperator('-');
  verifyValue(getAccum(), 71, 'After subtract Accum = 71');

  numberClick(3);
  // Check X and accum
  verifyValue(getX(), 3, 'X = 3');

  doOperator('*');
  verifyValue(getAccum(), 71, 'After subtract Accum = 71');
  verifyValue(getAccum(), 273, 'After multiply Accum = 273');

  numberClick(2);
  // Check X and accum
  verifyValue(getX(), 2, 'X = 2');
			
  doOperator('=');
  // Check state
  // Check X and accum
  verifyValue(getAccum(), 142, 'After multiply Accum = 142');

  var tempOut = document.getElementById('test_output');
  var outLine = 'testAdd1: ' + numSuccess + ' pass, ' +  numFailure + ' fail. Failures = ' +
    failureList;
  tempOut.innerHTML = outLine;
  tempOut.value = outLine; 
}

function verifyValue(actualValue, expectedValue, testInfo) {
  if (actualValue == expectedValue) {
    numSuccess += 1;
  } else {
    numFailure += 1;
    failureList.push(testInfo + ': actualValue = ' + actualValue + ', expectedValue = ' +
      expectedValue);
  }
}
