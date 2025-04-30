function openModal() {
  const modal = document.getElementById("modal");
  modal.classList.remove("hidden");
  modal.classList.add("scale-100");
}

function closeModal() {
  const modal = document.getElementById("modal");
  modal.classList.add("hidden");
  modal.classList.remove("scale-100");
}

function submitLink(event) {
  event.preventDefault();
  const link = document.getElementById("conferenceLink").value;
  if (link) {
    window.location.href = link; // Redirect to the provided link
  }
}
