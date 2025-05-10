const searchbar = document.getElementById("userSearch");

searchbar.addEventListener("keyup", function () {
  const list = document.getElementById("list");
  const inputText = searchbar.value.trim(); // Get and clean input
  console.log("Triggered");

  if (inputText === "") {
    console.log("No input");
    list.classList.remove("hidden");
  } else {
    list.classList.add("hidden");

    fetch(`/get_users/${encodeURIComponent(inputText)}`)
      .then((response) => response.json())
      .then((data) => {
        console.log("Fetched users:", data);
        // Optionally: update the list here with data
      })
      .catch((error) => {
        console.error("Error fetching users:", error);
      });
  }
});
