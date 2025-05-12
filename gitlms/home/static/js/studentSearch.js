const searchbar = document.getElementById("userSearch");
const list = document.getElementById("list");
const slist = document.getElementById("slist");

searchbar.addEventListener("keyup", function () {
  const inputText = searchbar.value.trim();

  if (inputText === "") {
    slist.innerHTML = "";
    list.classList.remove("hidden");
  } else {
    list.classList.add("hidden");

    fetch(`/get_users/${encodeURIComponent(inputText)}`)
      .then((response) => response.json())
      .then((data) => {
        slist.innerHTML = ""; // Clear previous search results

        if (data.length === 0) {
          slist.innerHTML = "<p class='text-gray-500'>No users found.</p>";
          return;
        }

        data.forEach((user) => {
          const card = `
          <div class="flex items-center bg-white p-4 sm:p-6 rounded-lg shadow-md hover:shadow-xl transition-transform duration-300 transform hover:scale-105">
            <div class="w-14 h-14 sm:w-16 sm:h-16 mr-4 flex-shrink-0">
              <img src="${user.profilepicture}" class="w-full h-full rounded-full object-cover" />
            </div>
            <div class="text-sm sm:text-base">
              <h3 class="font-semibold text-blue-900">
                ${user.first_name} ${user.last_name}
              </h3>
              <p class="text-gray-600">Email: ${user.email}</p>
              <p class="text-gray-600">${user.role}</p>
            </div>
          </div>`;
          slist.insertAdjacentHTML("beforeend", card);
        });
      })
      .catch((error) => {
        console.error("Error fetching users:", error);
        slist.innerHTML = "<p class='text-red-500'>Error loading users.</p>";
      });
  }
});
