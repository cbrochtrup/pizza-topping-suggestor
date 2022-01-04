//////// Data Processing Code //////////

var SERVER_IP = 'jellyfishjunction.zapto.org'

var ERROR_TEXT = 'Ope, sorry! There was an error from server. Does Colin have it on?'


const get_sentiment_toppings = async (user_guess) => {
  console.log(mode)
  var mode = $( "#modeSelecter" ).val()
  var uri;
  if (mode == "feelings") {
    uri = 'http://' + SERVER_IP + '/top?feelings=' + user_guess
  } else {
    var arr = user_guess.split(",").map(function(item) {
        return item.trim();
    });
    const query_params = arr.join('&topping=')
    console.log(arr)
    uri = 'http://' + SERVER_IP + '/suggest?topping=' + query_params 
  }
  const encoded = encodeURI(uri);
  console.log(encoded);
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
        'PLACEHOLDER<br/>' + responseData['toppings'].slice(0, 3).join(', '))
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
  // $("#user").toggleClass('is-hidden');
  get_sentiment_toppings(userGuess);
  console.log(userGuess);
  if (userGuess.length > 2 && ! $('#userGuessButton').prop('disabled')) {
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
