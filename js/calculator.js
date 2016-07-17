// Javascript to support calculator functions.

// In progress: create the finite state machine.

 // Constants and operators
  const noOp = 'noOp';
  const op_add = "+";
  const op_sub = "-";
  const op_mul = "*";
  const op_div = "/";
  const op_eq = "=";
  const op_enter = "enter";
  const enterPoint = ".";
  const opClear = 'clear';
  const op_clear_x = "clear X";
  const op_clear_accum = "clear A";
  const op_enter_numeral = 'enter_numeral';
  const errorArg = 0;
  const noErrorArg = 1;
  
  const zeroPoint = "0.";
  const errorDisp = "*ERROR*";
  
  // Output region for testing
  var testOutArea = null;
  
  // The Cherokee numeral list
  var seqNumList = []
  
var FSM = function () {
  this.reset();
};

FSM.prototype.reset = function() {
  this.state = 0;
  this.accumulator = 0;  // Decimal value.
  this.xRegister = 0;  // Decimal value.
  this.pendingOp = noOp;
  // This accumulates the Sequoyah numerals.
  this.seqNumList = [];
  
  // Output region for testing
  this.testOutArea = null;
}

FSM.prototype.setOutputId = function(areaId) {
  this.testOutArea = document.getElementById(areaId);
}
 
FSM.prototype.FSMstep = function (input, value) {
    state = this.getFSMState();
    if (state == 0) {
      // Start State 0
     handleStartState0(input, value);
      return;
    }
    if (state == 1) {
      // Accum State
     handleAccumState1(input, value);
      return;
    } 
    if (state == 2) {
      // Compute State
	handleComputeState2(input, value);
	return;
    }
    if (state == 3) {
      // Error State
      // Handle state 3
      return;
    }
    if (state == 4) {
      // Point State - handle decimal separator
      // Handle state 3
      return;
    }
  }
  
FSM.prototype.getAccumulator = function() {
    return this.accumulator;
   }  
  // State variables for calculator.
  var accumulator = 0;
  var accum_set = false;
  var x_value = 0;
  var last_operation = null;  // 
  var pendingOp = noOp;
  var FSMstate = 0;  // Start State

  
  // The non-OOP version.
  // Initialize FSM. Accept ID for output.
  function initializeFSM(areaId) {
	testOutArea = document.getElementById(areaId);
	clearAccumState();
  }
  
  // Finish State Machine from https://www.clear.rice.edu/comp212/06-spring/labs/13/
  // Handle the Finite State Machine.
  function getFSMState() {
    return FSMstate;
  }
  function setFSMState(newState) {
    FSMstate = newState;
  }
  
  function FSMstep(input, value) {
    state = getFSMState();
    if (state == 0) {
      // Start State 0
      handleStartState0(input, value);
      return;
    }
    if (state == 1) {
      // Accum State
      handleAccumState1(input, value);
      return;
    } 
    if (state == 2) {
      // Compute State
	  handleComputeState2(input, value);
	  return;
    }
    if (state == 3) {
      // Error State
      // Handle state 3
      return;
    }
    if (state == 4) {
      // Point State - handle decimal separator
      // Handle state 3
      return;
    }
  }
  
  function handleStartState0(input, value) {
    if (input == op_clear_x) {
      return 1;  // OK.
    }
    if (input == op_enter_numeral && value == 0) {
      setDisplay('0');
	  clearAccumState();
      return 1;
    }
    if (input == op_enter_numeral && value != 0) {
      accumulate(value);
      setFSMState(1);
      return 1;
    }
    if (input == op_eq) {
      doPendingOp(noErrorArg);
      pendingOp = noOP;
	  return 1;
    }
    if (isEnterOp(input)) {
      doPendingOp();
      pendingOp = input;
	  setFSMState(2);
	  return 1;
    }
    if (input == enterPoint) {
      setDisplay(zeroPoint);
	  setFSMState(4);
	}    
    // INVALID for state 0.
    return -1;  
  }
  
  // State 1: AccumState - number is being entered.
  function handleAccumState1(input, value) {
    if (input == op_clear_x) {
	  clearAccumState();
	  setX(0);
      setFSMState(0);
      setOutput(testOutArea, getAccumulator());
      return 1;  // OK.
    }
    if (input == op_enter_numeral) {
      accumulate(value);
      setOutput(testOutArea, getX());
      return 1;
    }
    if (isEnterOp(input)) {
      doPendingOp(noErrorArg);
      pendingOp = input;
      setOutput(testOutArea, getAccumulator());
	  setFSMState(2);
	  return 2;
    }
    if (input == op_eq) {
      doPendingOp(noErrorArg);
      pendingOp = noOp;
      setOutput(testOutArea, getAccumulator());
	  setFSMState(0);
	  return 2;
    }
    if (input == enterPoint) {
      appendPoint();
	  setFSMState(4);
      setOutput(testOutArea, getX());
	  return 4;
    }
    // INVALID for state 1.
    return -1;
  }

  // State 2: ComputeState - number is being entered.
  function handleComputeState2(input, value) {
    if (input == op_clear_x) {
	  clearAccumState();
	  setX(0);
      setFSMState(0);
      setOutput(testOutArea, getX());
      return 1;  // OK.
    }
    if (input == op_eq) {
      // ARE THESE THE RIGHT ACTIONS?
      doPendingOp(noErrorArg);
      pendingOp = noOp;
      // Update the display of accum.
      setOutput(testOutArea, getAccumulator());
	  setFSMState(0);
	  return 2;
    }
    if (input == op_enter_numeral) {
      setX(value);
      if (value != 0) {
        accumulate(value);
      }
      setOutput(testOutArea, getX());
      // TODO: reaccumulateValue();
      return 1;
    }
    if (isEnterOp(input)) {
      doPendingOp(noErrorArg);
      pendingOp = input;
      setOutput(testOutArea, getAccumulator());
	  return 2;
    }    

    if (input == enterPoint) {
      setDisplay(zeroPoint);
      setOutput(testOutArea, getX());
	  setFSMState(4);
	}

    // INVALID for state 2.
    return -1;
  }

  function handleErrorState3(input, value) {
    if (input == op_clear_x) {
 	  setFSMState(0);
      setDisplay(0);
      return 1;  // OK.
    }
    if (input == op_enter_numeral && value == 0) {
      setDisplay('0');
	  clearAccumState();
      return 1;
    }

	// Otherwise ignore and stay in this state.
	setDisplay(errorDisp);
    return 3;  
  }

  // State 4: PointState - point just was entered.
  function handlePointState4(input, value) {
    if (input == enterPoint) {
	  // Do nothing
	  return 4;
    }
    if (input == op_clear_x) {
	  clearAccumState();
	  setX(0);
      setFSMState(0);
      setOutput(testOutArea, getAccumulator());
      return 1;  // OK.
    }
    if (input == op_enter_numeral) {
      accumulate(value);
      setOutput(testOutArea, getX());
      return 1;
    }
    if (isEnterOp(input)) {
      doPendingOp(noErrorArg);
      pendingOp = input;
      setOutput(testOutArea, getAccumulator());
	  setFSMState(2);
	  return 2;
    }
    if (input == op_eq) {
      doPendingOp(noErrorArg);
      pendingOp = noOp;
      setOutput(testOutArea, getAccumulator());
	  setFSMState(0);
	  return 2;
    }

    // INVALID for state 4.
    return -1;
  }

  function isEnterOp(input) {
    // If input is an operation +, -, *, /
    if (input == op_add || input == op_sub || input == op_mul || input == op_div) {
      return true;
    }
    return false; 
  }

  function doPendingOp() {
    // Something is already there.
    if (pendingOp == noOp) {
      return;
    }
    if (pendingOp == op_add) {
      newVal = accumulator + x_value;
    } else if (pendingOp == op_sub) {
      newVal = accumulator - x_value;
    } else if (pendingOp == op_mul) {
      newVal = accumulator * x_value;
    } else if (pendingOp == op_div) {
      newVal = accumulator / x_value;
    } else {
      newVal = Number.POSITIVE_INFINITY;  // This is probably an error.
    }
    setAccumulator(newVal);
    setDisplay(newVal);
  }
  
  // Append digit to value in accumulator. Update display.
  function accumulate(value) {
    seqNumList.push(value);
    // Compute the decimal value and put in accumulator.
    var digitalVal = numListToInteger(seqNumList);
    // OLD: setAccumulator(digitalVal);
    setX(digitalVal);
    // Show the value.
    setDisplay(getX());
  }
  
  function setDisplay(input) {
  	// TODO: Finish this.
  	if (typeof(input) == "number") {
    	// Convert digital accumulator to numList.
    	var numList = digitalToSequoah(accumulator);
    	setOutput(testOutArea, accumulator);  // For testing.
    	return;
  	}
  	// Otherwise, set output message.
  	setOutputMessage(input);
  	return;
  }

  function setOutput(area, value) {
    area.innerHTML = value;
    area.value = value;
  }
  
  function setOutputMessage(textToShow) {
	// TODO: Output to text area.
  }

  function clearAccumState() {
    accum_set = false;
    accumulator = 0;
    setAccumOutput(accumulator);
    FSMstate = 0;
  }

  function setAccumulator(val) {
    accumulator = val;
    accum_set = true;
    setAccumOutput(accumulator);
  }
  
  function getAccumulator() {
    return accumulator;
  }
    
  function setX(val) {
    x_value = val;
    setXOutput(x_value);
  }
  
  function getX() {
    return x_value;
  }
  
  function operatorSelection(op) {
    // Get the x value from globalNumList.
    x_value = compute_X_value(numList);
    
    if (op == op_clear_x) {
      setX(0);
      clearArea('text1');
      return;
    }
    if (op == op_clear_accum || op == opClear) {
      clearAccumState();
      return;
    }
    
    if (accum_set) {
      var newVal = null;
      // Something is already there.
      if (last_operation == op_add) {
        newVal = accumulator + x_value;
        clearArea('text1');
      } else if (last_operation == op_sub) {
        newVal = accumulator - x_value;
        clearArea('text1');
      } else if (last_operation == op_mul) {
        newVal = accumulator * x_value;
        clearArea('text1');
      } else if (last_operation == op_div) {
        newVal = accumulator / x_value;
        clearArea('text1');
      } else if (last_operation == op_eq) {
        // WHAT TO DO HERE?
	  }
	  setLastOp(last_operation);
	  last_operation = null;
      if (newVal != null) {
        setAccumulator(newVal);
        var new_list = digitalToSequoah(accumulator);
        num_list = new_list[0];
        updateChrOutput(num_list);
      }
    } else {
      // Accumulator is not set.
      setAccumulator(x_value);
      clearArea('text1');
    }
    last_operation = op;
  }

// Handle display
function enterDigital(val) {
  var new_list = digitalToSequoah(val);
  updateChrOutput(new_list[0]);
  setX(val);
  return new_list; 
}

function setXOutput(val) {
  accumArea = document.getElementById('x');
  accumArea.value = val;
  accumArea.innerHTML = val;
}

function setAccumOutput(val) {
  accumArea = document.getElementById('accumulator');
  accumArea.value = val;
  accumArea.innerHTML = val;
}
