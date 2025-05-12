const searchbar = document.getElementById("userSearch");
const list = document.getElementById("list");
const slist = document.getElementById("slist");

searchbar.addEventListener("keyup", function () {
  const inputText = searchbar.value.trim();

  if (inputText === "") {
    slist.innerHTML = "";
    list.classList.remove("hidden");
    return;
  }

  list.classList.add("hidden");
  slist.innerHTML = ""; // Clear previous results

  fetch(`/get_users/${encodeURIComponent(inputText)}`)
    .then((response) => response.json())
    .then((data) => {
      if (!Array.isArray(data) || data.length === 0) {
        slist.innerHTML = `<p class="text-gray-500">No users found.</p>`;
        return;
      }

      // Optionally group by role
      const grouped = {
        Admin: [],
        Moderator: [],
        User: [],
      };

      data.forEach((user) => {
        if (user.role === "admin") grouped.Admin.push(user);
        else if (user.role === "mod") grouped.Moderator.push(user);
        else if (user.role === "user") grouped.User.push(user);
      });

      const renderUsers = (users, title, appointRole) => {
        if (users.length === 0) return;

        const header = document.createElement("h1");
        header.className = "text-2xl sm:text-4xl font-bold text-blue-900 mb-4";
        header.textContent = title;
        slist.appendChild(header);

        users.forEach((user) => {
          const userCard = `
          <div class="flex flex-col sm:flex-row sm:items-center bg-white p-4 sm:p-6 rounded-lg shadow-md hover:shadow-xl transition-transform duration-300 transform hover:scale-[1.02] relative">
            <div class="w-16 h-16 mb-4 sm:mb-0 sm:mr-4 mx-auto sm:mx-0">
              <img src="${
                user.profilepicture
              }" class="w-full h-full rounded-full object-cover" />
            </div>
            <div class="flex-grow text-center sm:text-left">
              <h3 class="text-base sm:text-lg font-semibold text-blue-900">${
                user.first_name
              } ${user.last_name}</h3>
              <p class="text-gray-600 text-sm sm:text-base">Email: ${
                user.email
              }</p>
              <p class="text-gray-600 text-sm sm:text-base">${user.role}</p>
            </div>
            <button onclick="showAppointModal('${appointRole}', '${
            user.id
          }', userInstituteId)"
              class="bg-gray-200 hover:bg-gray-300 p-2 rounded-full focus:outline-none mt-4 sm:mt-0 sm:ml-4">
              Assign ${
                appointRole.charAt(0).toUpperCase() + appointRole.slice(1)
              }
            </button>
          </div>
          `;
          slist.insertAdjacentHTML("beforeend", userCard);
        });
      };

      renderUsers(grouped.Admin, "Admins", "admin");
      renderUsers(grouped.Moderator, "Moderators", "moderator");
      renderUsers(grouped.User, "Users", "moderator"); // You can change "moderator" if needed
    })
    .catch((error) => {
      console.error("Error fetching users:", error);
      slist.innerHTML = `<p class="text-red-500">Something went wrong.</p>`;
    });
});
