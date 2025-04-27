// Open a WebSocket connection
const notificationSocket = new WebSocket(
  "ws://" + window.location.hostname + ":8001/ws/notifications/"
);

notificationSocket.onopen = function (e) {
  console.log("WebSocket connection established");
};

notificationSocket.onerror = function (e) {
  console.error("WebSocket error:", e);
};

notificationSocket.onclose = function (e) {
  console.error("WebSocket closed unexpectedly", e);
};

// When receiving a message from the WebSocket
notificationSocket.onmessage = function (e) {
  try {
    console.log("Message event triggered!");
    const data = JSON.parse(e.data);
    console.log("Notification received:", data);

    // Create a new notification element
    const notificationElement = document.createElement("div");
    notificationElement.classList.add(
      "bg-white",
      "rounded-lg",
      "shadow-xl",
      "p-6",
      "w-full",
      "mx-auto"
    );

    // Check if the notification type is not 'inf' (info type)
    if (data.notification.type !== "inf") {
      notificationElement.classList.add("border-l-4", "border-blue-500");

      notificationElement.innerHTML = `
          <div class="flex justify-between items-start">
            <div class="flex-1">
              <h3 class="font-medium text-gray-900">
                New ${data.notification.type} Request
              </h3>
              <p class="text-gray-600 mt-1">${data.notification.message}</p>
              <div class="flex items-center mt-3 text-sm text-gray-500">
                <i class="far fa-clock mr-1"></i>
                <span>now </span>
              </div>
            </div>
            <div class="ml-4 flex flex-col items-end">
              <div class="flex space-x-2">
                <button
                  onclick="window.location.href='${baseUrl}/notifications/approve/${data.notification.id}';"
                  class="px-4 py-2 bg-green-100 text-green-800 rounded-md hover:bg-green-200 transition-colors"
                >
                  Approve
                </button>
                <button
                  onclick="window.location.href='${baseUrl}/notifications/reject/${data.notification.id}';"
                  class="px-4 py-2 bg-red-100 text-red-800 rounded-md hover:bg-red-200 transition-colors"
                >
                  Reject
                </button>
              </div>
              <!-- View Details Link -->
              <a
                href="${baseUrl}/notifications/view/${data.notification.id}"
                class="text-blue-600 text-sm hover:underline mt-2"
              >
                View Details
              </a>
            </div>
          </div>
        `;
    } else {
      // If the notification type is 'inf', create a different style
      notificationElement.classList.add("border-l-4", "border-transparent");

      notificationElement.innerHTML = `
          <div class="flex justify-between items-start">
            <div class="flex-1">
              <h3 class="font-medium text-gray-900">Approval Notification</h3>
              <p class="text-gray-600 mt-1">${data.notification.message}</p>
              <div class="flex items-center mt-3 text-sm text-gray-500">
                <i class="far fa-clock mr-1"></i>
                <span>now </span>
              </div>
            </div>
          </div>
        `;
    }

    // Append the new notification to the container
    document
      .querySelector(".overflow-y-auto .space-y-4")
      .prepend(notificationElement);
  } catch (err) {
    console.error("Error handling message:", err);
  }
};
