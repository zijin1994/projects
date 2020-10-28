/**display friend list buttons and chatbox, messages**/
function display_form_buttons(value, name){
  var buttons = document.getElementById("friendlist_popup_buttons");
  document.querySelector('h1').innerHTML = value;
  document.getElementById("message_send").name = name;
  document.getElementById("chatpop").style.display = "block";
  buttons.style.display = "block";
  var received_messages = document.getElementsByClassName("received_messages");
  var sent_messages = document.getElementsByClassName("sent_messages");
  if (received_messages){
    var i;
    for (i = 0; i < received_messages.length; i++){
      if (received_messages[i].getAttribute("name")==name){
      received_messages[i].style.display = "block";
      }
      else {
      received_messages[i].style.display = "none";
      }
    }
  }

  if (sent_messages){
    var i;
    for (i = 0; i < sent_messages.length; i++){
      if (sent_messages[i].getAttribute("name")==name){
        sent_messages[i].style.display = "block";
      }
      else {
        sent_messages[i].style.display = "none";
      }
    }
  }
}


/**hide chat room**/
function close_chatbox(){
  document.getElementById("friendlist_popup_buttons").style.display = "none";
  document.getElementById("chatpop").style.display = "none";
}
