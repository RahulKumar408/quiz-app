

var totalQuestion = totalQuestion;
console.log(totalQuestion);
const submit = document.getElementById("submit-btn");
$(document).ready(function() {
  var currentQuestion = 1;
  showQuestion(currentQuestion);

  

  $('#next-btn').click(function() {
    // Increment the current question index
    if (currentQuestion < totalQuestion) {
      currentQuestion++;
    }

    if (currentQuestion === totalQuestion) {
      $('#submit-btn').removeAttr('disabled');
    }
    showQuestion(currentQuestion);
  });

  $('#previous-btn').click(function() {
    if (currentQuestion > 1) {
      currentQuestion--;
    }
  
    showQuestion(currentQuestion);
  });


  var rad = $('.form-check-input');
  var prev = null;
  for (var i = 0; i < rad.length; i++) {
      rad[i].addEventListener('change', function() {
        if(this.checked){
          console.log(this.value);
          console.log(this.checked);
          console.log(this.id);
          console.log(this.name);
        }
    });
}

});

function showQuestion(questionIndex) {
  $('.question-card').hide();
  
  $('#question-' + questionIndex).show();
  
  $('#current-question').text(questionIndex);
  
}




// Update the time remaining every second
var timeRemaining = 600; 
setInterval(updateTimeRemaining, 1000);

function updateTimeRemaining() {
  var minutes = Math.floor(timeRemaining / 60);
  var seconds = timeRemaining % 60;
  document.getElementById("time").textContent = minutes.toString().padStart(2, "0") + ":" + seconds.toString().padStart(2, "0");

  timeRemaining--;
  if (timeRemaining < 0) {
    // Time's up, handle logic here
  }
}
