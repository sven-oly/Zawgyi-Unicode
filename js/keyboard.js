// Utilities and other functions for keyboard control

// Global for control of keyboard.
    var controller, visible = true;

    function setupKeyboard(outputAreaId, langList, selectKeyboardId) {
      var input = document.getElementById(outputAreaId);
      controller = new i18n.input.keyboard.Keyboard();
      for (langId in langList) {
        controller.loadLayout(langId);
      }

      controller.reposition(input, 2, 0, [1, 0, 0, 0]);
      controller.register(input);
      controller.addEventListener('kc', function() { visible = false; });
      input.focus();
      var selector = document.getElementById(selectKeyboardId);
      onLayoutSelected(selector, controller, outputAreaId);
      return controller;
    }

  function onLayoutSelected(selector, this_controller, outputId) {
    var layoutCode = selector.value;
    if (this_controller) {
      this_controller.activateLayout(layoutCode);
    } else {  // The global.
      controller.activateLayout(layoutCode);
    }
    document.getElementById(outputId).focus();
  }

  // TODO: Add font size.

  // TODO: Add font selection.
      //onFontSelected(document.getElementById('selectFont'), 't1');

  function toggleKeyboard() {
    if (controller) {
      controller.setVisible(visible = !visible);
    }
  }
