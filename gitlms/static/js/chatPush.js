// Open a WebSocket connection
const CommChatSocket = new WebSocket(
  "wss://" + window.location.hostname + `:8001/ws/commChat/${ins_id}`
);

CommChatSocket.onopen = function (e) {
  console.log("CommChat WebSocket connection established");
};

CommChatSocket.onerror = function (e) {
  console.error(" CommChat WebSocket error:", e);
};

CommChatSocket.onclose = function (e) {
  console.error(" CommChat WebSocket closed unexpectedly", e);
};

// When receiving a message from the WebSocket
CommChatSocket.onmessage = function (e) {
  try {
    const data = JSON.parse(e.data);
    const chatContainer = document.getElementById("chat-messages");

    const isCurrentUser = data.sender.id == currentUserId;

    const messageHtml = isCurrentUser
      ? `
      <div class="flex items-start justify-end m-9">
        <div class="ml-4 flex flex-col items-end">
          <div class="flex items-center space-x-2 mr-2">
            <span class="text-lg font-semibold text-gray-800">${currentUserName}</span>
            <span class="text-xs text-gray-400">${formatTime(
              data.timestamp
            )}</span>
          </div>
          <p class="text-sm text-blue-600 mt-1 leading-relaxed">
            ${escapeHtml(data.message)}
          </p>
        </div>
        <div class="flex-shrink-0">
          <img
            src="${currentUserAvatar}"
            alt="Receiver Avatar"
            class="h-12 w-12 rounded-full border-2 border-blue-500"
          />
        </div>
      </div>
    `
      : `
      <div class="flex items-start relative m-9">
        <div class="relative">
          <img
            src='${data.sender.profilepicture}'
            alt="Sender Avatar"
            class="h-12 w-12 rounded-full border-2 border-blue-500 cursor-pointer sender-avatar"
            onclick="toggleOptions('options-${data.sender.id}')"
          />
          <div id="options-${
            data.sender.id
          }" class="options-menu absolute left-0 top-12">
            <button class="text-gray-700 hover:text-blue-500">View Profile</button>
            <button class="text-gray-700 hover:text-blue-500">Block User</button>
            <button class="text-gray-700 hover:text-blue-500">Mute Notifications</button>
          </div>
        </div>
        <div class="ml-4 flex flex-col">
          <div class="flex items-center space-x-2">
            <span class="text-lg font-semibold text-gray-800">${
              data.sender.name
            }</span>
            <span class="text-xs text-gray-400">${formatTime(
              data.timestamp
            )}</span>
          </div>
          <p class="text-sm text-gray-600 mt-1 leading-relaxed">
            ${escapeHtml(data.message)}
          </p>
        </div>
      </div>
    `;

    chatContainer.innerHTML += messageHtml;
    scrollChatToBottom(); // Optional helper
  } catch (err) {
    console.error("Error handling message:", err);
  }
};

function escapeHtml(unsafe) {
  return unsafe.replace(/[&<"']/g, function (m) {
    return {
      "&": "&amp;",
      "<": "&lt;",
      '"': "&quot;",
      "'": "&#039;",
    }[m];
  });
}

function formatTime(timestamp) {
  const date = new Date(timestamp);
  return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}
