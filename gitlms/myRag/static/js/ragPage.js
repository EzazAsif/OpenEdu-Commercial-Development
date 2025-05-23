// Open a WebSocket connection
const tutorAiSocket = new WebSocket(
  "ws://" + window.location.hostname + ":/ws/tutorai/"
);

tutorAiSocket.onopen = function (e) {
  console.log("tutorai WebSocket connection established");
};

tutorAiSocket.onerror = function (e) {
  console.error(" tutorai WebSocket error:", e);
};

tutorAiSocket.onclose = function (e) {
  console.error(" tutorai WebSocket closed unexpectedly", e);
};

const input = document.getElementById("user-input");
const imageInput = document.getElementById("image-input");
const button = document.getElementById("send-button");
const chat = document.getElementById("chat-area");
const form = document.getElementById("chat-form");

function escapeHTML(str) {
  const div = document.createElement("div");
  div.appendChild(document.createTextNode(str));
  return div.innerHTML;
}

// Update the input's value on typing
function handleInputChange() {
  input.value = input.value; // Make sure the input is not cleared
}

function sendMessage() {
  const msg = input.value.trim();
  const file = imageInput.files[0];

  // If no text and no image, do nothing
  if (!msg && !file) return;

  // If there's text, add user text bubble
  if (msg) {
    const escapedMsg = escapeHTML(msg);
    const userBubble = `
      <div class="flex items-start justify-end space-x-2">
        <div class="bg-blue-100 rounded-2xl px-4 py-2 text-sm max-w-xl shadow break-all-text">${escapedMsg}</div>
        <div class="h-10 w-10 rounded-full bg-blue-400 flex-shrink-0"></div>
      </div>`;
    chat.innerHTML += userBubble;

    // Send the message to the WebSocket
    if (tutorAiSocket.readyState === WebSocket.OPEN) {
      tutorAiSocket.send(JSON.stringify({ type: "text", message: msg }));
    } else {
      console.error("WebSocket not open. Message not sent.");
    }
  }

  // If there's an image, create an image bubble
  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      const imgSrc = e.target.result;
      const imgBubble = `
        <div class="flex items-start justify-end space-x-2">
          <div class="bg-blue-100 rounded-2xl p-2 max-w-xs shadow flex-shrink-0">
            <img src="${imgSrc}" alt="User upload" class="max-w-full max-h-48 rounded-lg" />
          </div>
          <div class="h-10 w-10 rounded-full bg-blue-400 flex-shrink-0"></div>
        </div>`;
      chat.innerHTML += imgBubble;

      // AI reply after image
      const aiBubble = `
        <div class="flex items-start space-x-2">
          <div class="h-10 w-10 rounded-full bg-gray-300 flex-shrink-0"></div>
          <div class="bg-gray-100 rounded-2xl px-4 py-2 text-sm max-w-xl shadow break-all-text">Nice image! How can I assist you with it?</div>
        </div>`;
      chat.innerHTML += aiBubble;

      // Send image as base64 to WebSocket
      if (tutorAiSocket.readyState === WebSocket.OPEN) {
        tutorAiSocket.send(JSON.stringify({ type: "image", dataURL: imgSrc }));
      } else {
        console.error("WebSocket not open. Image not sent.");
      }

      chat.scrollTop = chat.scrollHeight;
    };
    reader.readAsDataURL(file);
  } else {
    // AI reply after text message only
    const aiBubble = `
      <div class="flex items-start space-x-2">
        <div class="h-10 w-10 rounded-full bg-gray-300 flex-shrink-0"></div>
        <div class="bg-gray-100 rounded-2xl px-4 py-2 text-sm max-w-xl shadow break-all-text">That's a great question!</div>
      </div>`;
    chat.innerHTML += aiBubble;

    chat.scrollTop = chat.scrollHeight;
  }

  // Clear inputs
  input.value = "";
  imageInput.value = "";

  // Focus back on input
  input.focus();
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  sendMessage();
});

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});
