// Get modal and button elements
const openModalBtn = document.getElementById("openModalBtn");
const modal = document.getElementById("modal");
const closeModalBtn = document.getElementById("closeModalBtn");

// Open modal when the button is clicked
openModalBtn.addEventListener("click", () => {
  modal.classList.remove("hidden");
});

// Close modal when the close button is clicked
closeModalBtn.addEventListener("click", () => {
  modal.classList.add("hidden");
});

// Close modal when clicking outside the modal
window.addEventListener("click", (e) => {
  if (e.target === modal) {
    modal.classList.add("hidden");
  }
});
