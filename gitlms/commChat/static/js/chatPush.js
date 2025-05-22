// Open a WebSocket connection
const CommChatSocket = new WebSocket(
  "wss://" + window.location.hostname + `:443/ws/commChat/${ins_id}`
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
  <div class="flex items-end justify-end px-4 py-2">
    <div class="flex flex-col items-end max-w-[80%] space-y-1">
      <div class="flex items-center justify-end space-x-2 text-xs text-gray-500">
        <span>${formatTime(data.timestamp)}</span>
        <span class="font-medium text-gray-600">${currentUserName}</span>
      </div>
      <div
        class="bg-[#DCF8C6] text-gray-900 px-3 py-1.5 rounded-[18px] rounded-br-sm shadow-sm text-sm leading-tight whitespace-pre-wrap break-words inline-block"
        style="word-break: break-all"
      >
        ${escapeHtml(data.message)}
      </div>
    </div>
    <img
      src="${currentUserAvatar}"
      alt="Sender Avatar"
      class="h-6 w-6 ml-2 rounded-full border border-green-400"
    />
  </div>
  `
  : `
  <div class="flex items-start relative px-6 py-3">
    <div class="relative">
      <img
        src="${data.sender.profilepicture}"
        alt="Sender Avatar"
        class="h-10 w-10 rounded-full border-2 border-yellow-400 cursor-pointer shadow sender-avatar"
        onclick="toggleOptions('options-${data.id}')"
      />
      <div
        id="options-${data.id}"
        class="hidden absolute left-0 top-12 bg-white shadow-lg rounded-lg p-2 w-36 z-20"
      >
        <button class="w-full text-left text-gray-700 hover:text-yellow-500 py-1">
          View Profile
        </button>
        <button class="w-full text-left text-gray-700 hover:text-yellow-500 py-1">
          Block User
        </button>
        <button class="w-full text-left text-gray-700 hover:text-yellow-500 py-1">
          Mute Notifications
        </button>
      </div>
    </div>
    <div class="ml-3 flex flex-col max-w-sm">
      <div class="flex items-center space-x-2 mb-1">
        <span class="text-sm font-medium text-gray-700">${data.sender.name}</span>
        <span class="text-xs text-gray-400">${formatTime(data.timestamp)}</span>
      </div>
      <div
        class="bg-yellow-100 text-yellow-900 text-sm px-3 py-1.5 rounded-2xl rounded-tl-none shadow break-words whitespace-pre-wrap leading-tight min-h-[1.5rem]"
        style="word-break: break-all"
      >
        ${escapeHtml(data.message)}
      </div>
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
