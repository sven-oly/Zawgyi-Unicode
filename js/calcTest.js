// Testing the calculator.
var calc_test_data = [
  [[12, "+", 5, "="], 17],
  [[12, "*", 5, "="], 60],
  [[12, "-", 5, "="], 7],
  [[12, "/", 3, "="], 4],
  [[12, "+", 5, "+", 107, "="], 124],
  [[12, "*", 8, "-", 3, "="], 93],
  [[12, "*", 5, "-", 3, "="], 57],
  [[9, "*", 2, "*", 3, "-", 6, "+", 4, "="], 52],
  ];

function runAllTests() {
  var failCount = 0;
  var passCount = 0;
  var result = testCalc1();
  passCount += result[0];
  failCount += result[1];

  result = runCalTests();    
  passCount += result[0];
  failCount += result[1];
  
  var tempOut = document.getElementById('test_output');
  var outLine = 'Calc Test: ' + passCount + ' pass, ' +  failCount + ' fail';

  tempOut.innerHTML = outLine;
  tempOut.value = outLine;  	
}

function testCalc1() {
  var failCount = 0;
  var passCount = 0;

  clearArea('text1');
  clearAccumState();
  enterDigital(1);
  operatorSelection("+");
  enterDigital(2);
  operatorSelection("=");
  var result = getAccumulator();
  
  if (result == 3) {
    passCount += 1;
  } else {
    failCount += 1;
  }
  // Add 7 more.
  operatorSelection("+");
  enterDigital(7);
  operatorSelection("+");
  result = getAccumulator();
  
  if (result == 10) {
    passCount += 1;
  } else {
    failCount += 1;
  }
  
  return [passCount, failCount];
}

function runCalTests() {
  var failCount = 0;
  var passCount = 0;

  var failList = [];
  for (var i = 0; i < calc_test_data.length; i ++) {
    clearArea('text1');
    clearAccumState();
    setX(0);
    var result = runCalcTest(calc_test_data[i][0]);
    var expected = calc_test_data[i][1];
    if (result == expected) {
      passCount += 1;
    } else {
      failCount += 1;
      failList.push([i, calc_test_data[i], result]);
    }
  }
  return [passCount, failCount, failList];
}

function runCalcTest(calcData) {
  // Run the functions, then get the accumulator.
  for (var i = 0; i < calcData.length; i ++) {
    var item = calcData[i];
    if (typeof(item) == "number") {
      enterDigital(item);
    } else
    if (typeof(item) == "string") {
      operatorSelection(item);
    } else {
      // This is strange. What to do?
    }
  }
  var result = getAccumulator();
  return result;
}

// Test using key input functions instead of decimal values.
var calcKey_test_data = [
  [[12, "+", 5, "="], 17],
  [[12, "*", 5, "="], 60],
  [[12, "*", 5, "-"], 60],
  [[12, "-", 5, "="], 7],
  [[12, "/", 3, "="], 4],
  [[12, "+", 5, "+", 100, 7, "="], 124],
  [[12, "*", 8, "-", 3, "="], 93],
  [[12, "*", 5, "-", 3, "="], 57],
  [[9, "*", 2, "*", 3, "-", 6, "+", 4, "="], 52],
  [[1000, 400, 30, 7, "+", 60, 4, "-", "70", "9", "="], 1422],
  [[12, "clear X", 17, "*", 5, "-", 3, "="], 62],
  [[12, "clear X", 17, "*", 5, "-", 3, "+"], 62],
  [["clear A"], 0]
  ];
  

function runAllCalcTests() {
  var failCount = 0;
  var passCount = 0;
  var result = testCalc1();
  passCount += result[0];
  failCount += result[1];

  result = runAllCalcKeyTests();    
  passCount += result[0];
  failCount += result[1];
  
  var tempOut = document.getElementById('test_output');
  var outLine = 'Calc Test: ' + passCount + ' pass, ' +  failCount + ' fail';

  tempOut.innerHTML = outLine;
  tempOut.value = outLine;  	
}

function runAllCalcKeyTests() {
  var failCount = 0;
  var passCount = 0;

  var failList = [];
  for (var i = 0; i < calcKey_test_data.length; i ++) {
    clearArea('text1');
    clearAccumState();
    setX(0);
    var result = runCalcKeyTest(calcKey_test_data[i][0]);
    var expected = calcKey_test_data[i][1];
    if (result == expected) {
      passCount += 1;
    } else {
      failCount += 1;
      failList.push([i, calcKey_test_data[i], result]);
    }
  }
  return [passCount, failCount, failList];}

function runCalcKeyTest(calcData) {
  // Run the functions, then get the accumulator.
  for (var i = 0; i < calcData.length; i ++) {
    var item = calcData[i];
    if (typeof(item) == "number") {
      numberClick(item);  // TODO: Call the keyboard input function.
    } else
    if (typeof(item) == "string") {
      operatorSelection(item);
    } else {
      // This is strange. What to do?
    }
  }
  var result = getAccumulator();
  return result;
}