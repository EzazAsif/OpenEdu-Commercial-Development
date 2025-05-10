window.addEventListener("DOMContentLoaded", function () {
  const sidePopups = document.querySelectorAll(".side-popup");
  sidePopups.forEach((sidePopup) => {
    sidePopup.classList.remove("translate-x-full"); // Remove translate class to make it slide in
    sidePopup.classList.add("translate-x-0"); // Position it at the screen edge
  });
});

// Open a WebSocket connection
const PopupSocket = new WebSocket(
  "wss://" + window.location.hostname + ":8001/ws/notifications/"
);

PopupSocket.onopen = function (e) {
  console.log("Popup WebSocket connection established");
};

PopupSocket.onerror = function (e) {
  console.error("Popup WebSocket error:", e);
};

PopupSocket.onclose = function (e) {
  console.error("Popup WebSocket closed unexpectedly", e);
};

// When receiving a message from the WebSocket
PopupSocket.onmessage = function (e) {
  try {
    console.log("Message event triggered!");
    const data = JSON.parse(e.data);
    console.log("Notification received:", data);

    var body = document.body;
    var popUpElement = document.createElement("div");
    popUpElement.classList.add(
      "side-popup", // Add a common class for all popups
      "fixed",
      "top-6",
      "right-6",
      "max-h-[300px]",
      "w-[280px]",
      "bg-white",
      "rounded-xl",
      "shadow-2xl",
      "z-50",
      "transform",
      "translate-x-full", // Start with the element out of view
      "transition-transform",
      "duration-500",
      "ease-out",
      "border-l-4",
      "border-blue-500"
    );

    // Close button
    const closeButton = document.createElement("button");
    closeButton.classList.add(
      "absolute",
      "top-2",
      "right-2",
      "text-gray-400",
      "hover:text-gray-700",
      "text-xl",
      "font-bold",
      "focus:outline-none"
    );
    closeButton.innerHTML = "&times;";
    closeButton.onclick = function () {
      closePopUpElement(popUpElement); // Close the specific popup
    };

    // Notification content
    const contentDiv = document.createElement("div");
    contentDiv.classList.add("relative", "p-5");

    const title = document.createElement("h2");
    title.classList.add("text-lg", "font-semibold", "text-gray-800", "mb-2");
    title.textContent = "Notification";

    const message = document.createElement("p");
    message.classList.add("text-sm", "text-gray-600", "leading-relaxed");
    message.textContent = data.notification.message;

    // Append elements
    contentDiv.appendChild(closeButton);
    contentDiv.appendChild(title);
    contentDiv.appendChild(message);
    popUpElement.appendChild(contentDiv);
    body.appendChild(popUpElement);

    // Trigger the slide-in animation
    setTimeout(() => {
      popUpElement.classList.remove("translate-x-full");
      popUpElement.classList.add("translate-x-0"); // Slide in
    }, 50); // Small delay to ensure the element is added to DOM first
  } catch (err) {
    console.error("Error handling message:", err);
  }
};

// Close popup element function
function closePopUpElement(popUpElement) {
  popUpElement.classList.remove("translate-x-0");
  popUpElement.classList.add("translate-x-full");
  // Add a small delay before fully hiding
  setTimeout(() => {
    popUpElement.remove(); // Completely remove the popup after hiding
  }, 1000);
}
