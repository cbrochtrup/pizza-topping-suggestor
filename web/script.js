//////// Data Processing Code //////////
//////////////////////////////////////////////

var SERVER_IP = 'jellyfishjunction.zapto.org'

var ERROR_TEXT = 'Something went wrong... I will get a better error messages eventually'


const get_sentiment_toppings = async (user_guess) => {
  var mode = $( "#modeSelecter" ).val()
  var uri;
  var display_prefix;
  if (mode == "feelings") {
    uri = 'http://' + SERVER_IP + '/top?feelings=' + user_guess
    display_prefix = 'These toppings match your mood:'
  } else {
    var arr = user_guess.split(",").map(function(item) {
        return item.trim();
    });
    const query_params = arr.join('&topping=')
    uri = 'http://' + SERVER_IP + '/suggest?topping=' + query_params 
    display_prefix = 'These toppings are great with ' + user_guess + ':'
  }
  const encoded = encodeURI(uri);
  const response = fetch(encoded, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
    }
  })
  .then((response) => response.json())
  .then(responseData => {
    console.log(responseData)
    $('#feedback').html(
        display_prefix + '<br/><b>' + responseData['toppings'].slice(0, 3).join(', ') + '</b>')
  })
  .catch(error => {
    console.warn(error);
    $('#feedback').text(ERROR_TEXT);
  });
}

////// GUI & jQuery code ///////

// Disable button on startup in case game doesn't load
$(document).ready(function(){
  setUserInputButtonDisabled(true);
  $('#userInputField').val('');
});

function sendUserInput(){
  userGuess = $('#userInputField').val().toLowerCase();
  console.log(userGuess);
  if (userGuess.length > 2 && ! $('#userGuessButton').prop('disabled')) {
    $('#feedback').html('Designing toppings!')
    get_sentiment_toppings(userGuess);
    console.log('sending!');
    $('#userInputField').val('');
  }
}


// Send user definition to API, get scores
$(document).ready(function(){
  $('#userGuessButton').click(function(){ sendUserInput(); });
});


// Start a new game, get a new word list
$(document).ready(function(){
  $("#newGame").click(function(){
    $('#newGame').prop('disabled', true);
    sendUserInput();
    setInterval(function(){
      $('#newGame').prop('disabled', false);
    }, 3000)
    $('#userInputField').val('').focus().blur();
  });
});


$(document).on('keydown', function (event) {
  var inp = String.fromCharCode(event.keyCode);
  if (/[a-zA-Z ]/.test(inp)) {
    $('#userInputField').focus()
  }
});

$(document).ready(function(){
  $('#userInputField').on('keypress', function(e) {
    if (e.which == 13) {
      sendUserInput();
    }
  });
});


function setUserInputButtonDisabled(b){
  $('#userGuessButton').prop('disabled', b);
}

$.getJSON("pizza_ingredients.json", function(json) {
  var linked_output = []
  for (const [key, value] of Object.entries(json)) {
    linked_output = linked_output.concat(value)
  }
  data = linked_output
  availableTags = linked_output
});

$(document).ready(function(){
  $( "#userInputField" ).autocomplete({
    source: data,
  });
});
