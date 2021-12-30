//////// Data Processing Code //////////

var SERVER_IP = 'jellyfishjunction.zapto.org'

var ERROR_TEXT = 'Ope, sorry! There was an error from server. Does Colin have it on?'


const get_sentiment_toppings = async (user_guess) => {
  console.log('hi')
  const response = fetch('http://' + SERVER_IP + '/top', {
    method: 'GET',
    // body: JSON.stringify({"list_length": list_length}),
    headers: {
      // 'Content-Type': 'application/json',
      'Accept': 'application/json',
    }
  })
  .then((response) => response.json())
  .then(responseData => {
    console.log(responseData)
  })
  .catch(error => {
    console.warn(error);
    // On error, move to the next word
    $('#feedback').text(ERROR_TEXT);
  });
}

////// GUI & jQuery code ///////

// Disable button on startup in case game doesn't load
$(document).ready(function(){
  setUserInputButtonDisabled(true);
  $('#userInputField').val('');
});

var userGuess;
function sendUserInput(){
  userGuess = $('#userInputField').val();
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
    get_sentiment_toppings("TODO: pass me in");
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
