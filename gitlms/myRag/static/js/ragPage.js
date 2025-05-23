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
    const userBubble = document.createElement("div");
    userBubble.className = "flex items-start justify-end space-x-2";

    // Create the message bubble
    const messageDiv = document.createElement("div");
    messageDiv.className =
      "bg-blue-100 rounded-2xl px-4 py-2 text-sm max-w-xl shadow break-all-text";
    messageDiv.textContent = escapedMsg;

    // Create the avatar container
    const avatar = document.createElement("div");
    avatar.className =
      "h-10 w-10 rounded-full bg-blue-400 flex-shrink-0 overflow-hidden";

    // Create the user image
    const userImg = document.createElement("img");
    userImg.src = requestuserpicture;
    userImg.alt = "User avatar";
    userImg.className = "h-full w-full object-cover";

    // Append image to avatar, then all to userBubble
    avatar.appendChild(userImg);
    userBubble.appendChild(messageDiv);
    userBubble.appendChild(avatar);

    document.querySelector("#chat-area").appendChild(userBubble);

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

// Helper: sanitize and preserve line breaks
function sanitizeAndFormat(text) {
  const div = document.createElement("div");
  div.innerHTML = text; // parse the raw HTML

  // Remove all tags except <a>
  const allowedTags = ["A"];

  function sanitizeNode(node) {
    if (node.nodeType === Node.ELEMENT_NODE) {
      if (!allowedTags.includes(node.tagName)) {
        // Replace disallowed tags with their text content
        const textNode = document.createTextNode(node.textContent);
        node.parentNode.replaceChild(textNode, node);
      } else {
        // Allowed tag: sanitize attributes (only keep href)
        [...node.attributes].forEach((attr) => {
          if (attr.name !== "href") node.removeAttribute(attr.name);
          // Optional: also validate href value here to be safe
        });
        // Recursively sanitize children
        node.childNodes.forEach(sanitizeNode);
      }
    }
  }

  div.childNodes.forEach(sanitizeNode);

  // Now replace line breaks with <br>
  let html = div.innerHTML;
  html = html.replace(/\n/g, "<br>");

  return html;
}

tutorAiSocket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  const safeHtml = sanitizeAndFormat(data.message);
  const parser = new DOMParser();
  const doc = parser.parseFromString(safeHtml, "text/html");

  if (data.type === "answer") {
    const aiMessageWrapper = document.createElement("div");
    aiMessageWrapper.className = "flex items-start space-x-2";

    const avatar = document.createElement("div");
    avatar.className =
      "h-10 w-10 rounded-full bg-gray-300 flex-shrink-0 overflow-hidden";

    const textContainer = document.createElement("div");
    textContainer.className =
      "bg-gray-100 rounded-2xl px-4 py-2 text-sm max-w-xl shadow break-words";

    aiMessageWrapper.appendChild(avatar);
    aiMessageWrapper.appendChild(textContainer);
    chat.appendChild(aiMessageWrapper);
    chat.scrollTop = chat.scrollHeight;

    const nodes = [...doc.body.childNodes];
    let nodeIndex = 0;
    let wordIndex = 0;
    let currentTextWords = [];
    let textNode = null;

    function typeNext() {
      if (nodeIndex >= nodes.length) {
        localStorage.setItem("cachedChat", chat.innerHTML);
        return;
      }

      const node = nodes[nodeIndex];

      if (node.nodeType === Node.TEXT_NODE) {
        if (currentTextWords.length === 0) {
          currentTextWords = node.textContent.split(/\s+/);
          wordIndex = 0;
          textNode = document.createTextNode("");
          textContainer.appendChild(textNode);
        }

        if (wordIndex < currentTextWords.length) {
          textNode.textContent += currentTextWords[wordIndex] + " ";
          chat.scrollTop = chat.scrollHeight;
          wordIndex++;
          setTimeout(typeNext, 200);
        } else {
          currentTextWords = [];
          nodeIndex++;
          setTimeout(typeNext, 200);
        }
      } else if (node.nodeType === Node.ELEMENT_NODE) {
        textContainer.appendChild(node.cloneNode(true));
        chat.scrollTop = chat.scrollHeight;
        nodeIndex++;
        setTimeout(typeNext, 200);
      } else {
        nodeIndex++;
        setTimeout(typeNext, 200);
      }
    }

    typeNext();
  } else if (data.type === "error") {
    console.error("Error:", data.message);
  }
};

// Load cached chat HTML on page load
document.addEventListener("DOMContentLoaded", () => {
  const cachedChat = localStorage.getItem("cachedChat");
  if (cachedChat && chat) {
    chat.innerHTML = cachedChat;
    chat.scrollTop = chat.scrollHeight;
  }
});
