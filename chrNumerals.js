// Cherokee numerals computations.
// Same as the Python backend code.

var reducers = [100, 1000, 1e6, 1e9, 1e12, 1e15, 1e18];

var numeralValues = [1e18, 1e15, 1e12, 1e9, 1e6, 1000,
    100, 90, 80, 70, 60, 50, 40, 30, 20,
    19, 18, 17, 16, 15, 14, 13, 12, 11, 10,
    9, 8, 7, 6, 5, 4, 3, 2, 1, 0];

function cleanUpListDeletions(l1, l2) {
  // Remove items where l1[i] == -1.
  i = len(l1) - 1;
  while (i >= 0) {
    if (l1[i] == -1) {
      l1.splice(i, 1);
      l2.splice(i, 1);
    }
    i -= 1;
  }
        
function numListToInteger(numList) {
  // a. scan for add small
  // b. scan for multiply by hundreds
  // c. scan for add to hundreds
  // d. multiply 10^N from left
  // e. add all 
  var working = numList.slice();
  var tags = numList.slice();

  //# a. scan for add small
  start = 0;
  limit = working.length;
  sum = 0;
  while (start < limit) {
    end = start;
    while (end < limit && working[end] < 100) {
      sum += working[end];
      end += 1;
    }
    if (end > start) {
      working[start] = sum;
      for (i = start + 1; i < end; i ++) {
        tags[i] = -1; 
      sum = 0;
    }
    start += 1;
  }  
  cleanUpListDeletions(tags, working);
  // logging.info('** Small added: %s' % working)
            
  // b. scan for multiply hundreds
  start = 0;
  limit = working.length;
  while (start < limit) {
    if (working[start - 1] < 100 && working[start] == 100) {
      working[start] = working[start - 1] * working[start];
      tags[start-1] = -1;
    }
    start += 1;
  }
  cleanUpListDeletions(tags, working);
  // logging.info('** 100 times: %s' % working)    

  // c. scan for add to hundreds
  start = 0;
  limit = working.length;
  while (start < limit) {
    if (tags[start - 1] == 100 && tags[start] < 100) {
      working[start] = working[start - 1] + working[start];
      tags[start-1] = -1;
    }
    start += 1
  }
  cleanUpListDeletions(tags, working);
  // logging.info('** 100s added: %s' % working)    

  // d. scan for multiply 10^N
  start = 0;
  limit = working.length;
  while (start < limit) {
    if (tags[start - 1] <= 100 && tags[start] > 100) {
      working[start] = working[start - 1] * working[start];
      tags[start-1] = -1;
    }
    start += 1;
  }
  cleanUpListDeletions(tags, working);
  //logging.info('** 10^N times: %s' % working)         

  // Add the results if needed
  grandSum = 0;
  for (i = 0; i < working.length; i ++) {
    grandSum += working[i];
  }
  return grandSum;
}

function numListToInteger_OLD(numList) {
  // a. multiply left from hundreds
  // b. add right from hundreds
  // c. multiply left from thousands
  // d. add right from thousands
  // e. add all 
  var working = numList.slice();
  var tags = numList.slice();
  // Add front first
  // Scan forward, adding until 1000, 1e6, etc.
  var reducer = reducers[0];
  var sum = 0;
  var i = 0;
  var start = i;
  while (i < working.length && tags[i] < reducer) {
    sum += working[i];
    i += 1;
    if (i > start) {
      working[i-1] = sum;
      working.splice(start, i - start - 1);
      tags.splice(start, i - start - 1);
    }
  }

  var reduceIndex = 0;
  while (reduceIndex < reducers.length && working.length > 1) {
    reducer = reducers[reduceIndex]
    i = 0
    while (i < working.length) {
      if (working[i] == reducer) {
        if (i > 0 && tags[i-1] < reducer) {
          working[i] *= working[i-1];
          working.splice(i-1, 1);
          tags.splice(i-1, 1);
          // i stays the same
        } else {
          i += 1;
        }
        // Scan forward, adding until 1000, 1e6, etc.
        sum = working[i-1];
        start = i;
        while (i < working.length && tags[i] < reducer) {
          sum += working[i];
          i += 1;
        }
        if (i > start) {
          working[start-1] = sum;
          working.splice(start, i - start - 1);
          tags.splice(start, i - start - 1);
          i = start + 1;
        }
      } else {
        i += 1;
      }
    }      
    reduceIndex += 1;    
  }
     
  // Add the results if needed
  grandSum = 0;
  for (i = 0; i < working.length; i ++) {
    grandSum += working[i];
  }
  // Should be done, with answer in the single element.
  return grandSum;
}

// Process the input numeral, outputting a list of count and numerals.
function digitalToSequoah(decimalNum) {

  // Returns a list of (value) of the decoded number in Sequoyah's numerals
  result = [];
  resultImage = [];
  //logging.info('---------- in = %d' % decimalNum)

  if (decimalNum == 0) {
    result = [0];
    resultImage = ['0'];
    return (result, resultImage);
  }
  
  if (decimalNum < 0) {
    remaining = -decimalNum;
    result.append(-1);
    resultImage = ['-1'];
  } else {
    remaining = decimalNum;
  }
  
  index = 0;
  count = 0;
  // logging.info('---------- in = %d' % decimalNum)
  while (remaining > 0 && index < numeralValues.length && count < 100) {
    while (remaining >= numeralValues[index]) {
      //logging.info(' index: %d, value[index]: %d, count: %d' %
      //  (index, numeralValues[index], count))
      count += 1;
      remaining -= numeralValues[index];
    }
    if (count > 0) {
      if (count == 1) {
        resultImage.push(imgArrayNames[index]);
        result.push(numeralValues[index]);
      } else {
        prefix = digitalToSequoah(count);
        if (prefix.prop && prefix.prop.constructor === Array) {
          logging.info(prefix);
          resultImage.extend(prefix[1]);
          result.extend(prefix[0]);
        } else {
          resultImage.push(prefix[1]);
          result.push(parseInt(prefix[0]));
        }
        resultImage.push(imgArrayNames[index]);
        result.push(numeralValues[index]);
      }
    }
      //logging.info('  result = %s' % (numeralValues[index]))
    count = 0;
    index += 1;
  }

  //logging.info('CHR version = %s' % resultImage)
  //logging.info('CHR result  = %s' % result)
  return [result, resultImage]  // Both the numbers and the strings.
}

// ------------------------ TESTS ----------------------
var chrTestSets = [	
  [[0], 0],
  [[1, 1], 2],
  [[20,2], 22],
  [[30, 1000, 7, 100, 50, 6], 30756],
  [[3, 100, 7], 307],
  [[100, 70, 9, 1000], 179000],
  [[6, 1000, 6, 100, 60, 6], 6666],
  [[50, 8, 1000, 40], 58040],
  [[100, 2, 1e6, 3, 1000, 4, 100, 50, 6], 102003456],
  [[17, 1e12, 8, 1000, 1], 17000000008001],
  [[1e9, 20, 1e6, 30, 4, 1000, 5, 100, 60, 7], 1020034567],
  [[7, 1000000000000, 20, 1, 1000000000, 30, 2, 1000000, 30, 9, 1000, 5, 100, 60, 7],
    7021032039567],
  [[9, 1e12, 9, 100, 80, 7, 1e3, 30], 9000000987030], 
  [[20, 3, 1000, 4], 23004]
  ];
  
// Tests num lists to integers.
function testChrToDec() {
  failCount = 0;
  passCount = 0;

  resultList = []
  for (i = 0; i < chrTestSets.length; i ++) {
    test = chrTestSets[i];
    var t0 = chrTestSets[i][0];
    var t1 = chrTestSets[i][1];
    result = numListToInteger(t0);
    if (compareLists(result, t1)) {
      passCount += 1;
      resultStatus = 'PASS';
    } else {
      failCount += 1;
      resultStatus ='FAIL';
    }
    resultList.push([resultStatus, test, result]);
  }
  return ('Test CHR to Dec', (passCount, failCount), resultList);
}

function compareLists(l1, l2) {
  if (l1.length != l2.length) {
    return false;
  }
  for (i = 0; i < l1.length; i++) {
    if (l1[i] != l2[i]) {
      return false;
    }
  }
  return true;
}

// Tests integers to num lists.
function testDecToChr() {
  failCount = 0;
  passCount = 0;

  resultList = [];
  for (i = 0; i < chrTestSets.length; i ++) {
    test = chrTestSets[i];
    var t0 = chrTestSets[i][0];
    var t1 = chrTestSets[i][1];
    resultList = digitalToSequoah(t1);
    result = resultList[0];
    if (compareLists(result, t0)) {
      passCount += 1;
      resultStatus = 'PASS';
    } else {
      failCount += 1;
      resultStatus ='FAIL';
    }
    resultList.push([resultStatus, test, result]);
  }
  return ('Test decimal to CHR', (passCount, failCount), resultList);
}