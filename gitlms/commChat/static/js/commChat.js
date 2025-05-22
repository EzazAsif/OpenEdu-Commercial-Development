function scrollChatToBottom() {
  const chat = document.getElementById("chat-messages");
  if (chat) {
    console.log(chat.scrollHeight);
    chat.scrollTop = chat.scrollHeight;
  }
}

// Scroll on page load
window.addEventListener("load", scrollChatToBottom);

// Toggle options menu for sender
function toggleOptions(id) {
  const menu = document.getElementById(id);
  menu.style.display = menu.style.display === "block" ? "none" : "block";
}

// Prevent form submission and handle sending message with attachment
function sendMessage(event) {
  event.preventDefault();

  const messageInput = event.target.querySelector('input[type="text"]');
  const message = messageInput.value.trim();

  if (!message) return; // Do not send empty messages

  console.log("Message:", message);
  CurrentUser = {
    id: currentUserId,
    name: currentUserName,
    profilepicture: currentUserAvatar,
  };
  // Construct the payload
  const payload = {
    type: "chat_message",
    sender: CurrentUser,
    message: message,
    timestamp: new Date().toISOString(),
  };

  // Send message to the WebSocket
  if (CommChatSocket.readyState === WebSocket.OPEN) {
    CommChatSocket.send(JSON.stringify(payload));
  } else {
    console.error("WebSocket is not open. Message not sent.");
  }

  // Reset the input field
  messageInput.value = "";
  setTimeout(scrollChatToBottom, 100); // wait for DOM update
}
