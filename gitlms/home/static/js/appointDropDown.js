// Function to show the appoint modal
function showAppointModal(role, userId, userInstituteId) {
  selectedUserId = userId; // Store the selected user's ID
  console.log(
    "Show appoint modal for userId:",
    userId,
    "with instituteId:",
    userInstituteId
  );
  document.getElementById("appointModal").classList.remove("hidden");
  document.getElementById("roleSelect").value = "assign";

  // Fetch institutes and populate the institute dropdown
  fetchInstitutes(userInstituteId);
  // Fetch departments based on the userInstituteId immediately
  if (userInstituteId) {
    fetchDepartmentsByInstitute(userInstituteId);
  }
}

// Function to close the appoint modal
function closeAppointModal() {
  console.log("Closing appoint modal");
  document.getElementById("appointModal").classList.add("hidden");
}

// Function to fetch institutes from the server
function fetchInstitutes(userInstituteId) {
  console.log("Fetching institutes...");
  fetch("/get_institutes/") // Endpoint to fetch institutes
    .then((response) => response.json())
    .then((data) => {
      const instituteSelect = document.getElementById("instituteSelect");
      instituteSelect.innerHTML = '<option value="">Select Institute</option>'; // Reset options

      data.forEach((institute) => {
        const option = document.createElement("option");
        option.value = institute.id;
        option.textContent = institute.name;

        // Lock the dropdown to the selected institute if userInstituteId is provided
        if (institute.id == userInstituteId) {
          option.selected = true;
          instituteSelect.disabled = true; // Lock the institute dropdown for everyone
        }

        instituteSelect.appendChild(option);
      });
    })
    .catch((error) => {
      console.error("Error fetching institutes:", error);
    });
}

// Function to fetch departments by selected institute
function fetchDepartmentsByInstitute(instituteId) {
  console.log("Fetching departments for instituteId:", instituteId);
  fetch(`/get_departments/${instituteId}`)
    .then((response) => response.json())
    .then((data) => {
      const departmentSelect = document.getElementById("departmentSelect");
      departmentSelect.innerHTML =
        '<option value="">Select Department</option>'; // Reset options

      data.forEach((department) => {
        const option = document.createElement("option");
        option.value = department.id;
        option.textContent = department.name;

        // Lock the department if department.id matches the requestUserDepartment
        if (department.id == requestUserDepartment) {
          option.selected = true; // Pre-select the matching department
          departmentSelect.disabled = true; // Lock the department dropdown
          // Update the hidden field with the department ID
          document.getElementById("departmentIdHidden").value = department.id;
          console.log("Department locked to:", department.name);
        }

        departmentSelect.appendChild(option);
      });

      departmentSelect.disabled = false; // Enable department selection if not locked
      console.log("Departments loaded:", data);

      // Trigger course fetching if the department is pre-selected or unlocked
      const preSelectedDepartmentId = departmentSelect.value;
      if (preSelectedDepartmentId) {
        fetchCourses(preSelectedDepartmentId);
      }
    })
    .catch((error) => {
      console.error("Error fetching departments:", error);
    });
}

// Event listener for department selection
document
  .getElementById("departmentSelect")
  .addEventListener("change", function () {
    const departmentId = this.value;
    console.log("Department selected:", departmentId);
    if (departmentId) {
      // Fetch courses when department is selected
      fetchCourses(departmentId);
    } else {
      // Reset and disable course selection if no department is selected
      resetCourseSelection();
    }
  });

// Function to fetch courses for the selected department
function fetchCourses(departmentId) {
  console.log("Fetching courses for departmentId:", departmentId);
  fetch(`/get_courses_by_department/${departmentId}/`)
    .then((response) => response.json())
    .then((data) => {
      const courseSelect = document.getElementById("courseSelect");
      courseSelect.innerHTML = '<option value="">Select Course</option>'; // Reset options

      data.forEach((course) => {
        const option = document.createElement("option");
        option.value = course.id;
        option.textContent = `${course.course_code} - ${course.course_name}`;
        courseSelect.appendChild(option);
      });

      courseSelect.disabled = false; // Enable course selection
      console.log("Courses loaded:", data);
    })
    .catch((error) => {
      console.error("Error fetching courses:", error);
    });
}

// Function to reset course dropdown
function resetCourseSelection() {
  console.log("Resetting course selection.");
  document.getElementById("courseSelect").innerHTML =
    '<option value="">Select Course</option>';
  document.getElementById("courseSelect").disabled = true;
}

// Function to handle role change
function roleChanged() {
  const role = document.getElementById("roleSelect").value;
  const instituteSelect = document.getElementById("instituteSelect");
  const departmentSelect = document.getElementById("departmentSelect");
  const courseSelect = document.getElementById("courseSelect");

  console.log("Role changed to:", role);

  // Always lock the institute select if userInstituteId is set
  instituteSelect.classList.remove("hidden"); // Always show institute dropdown

  if (role === "user") {
    // Hide department and course selections for users
    departmentSelect.classList.add("hidden");
    courseSelect.classList.add("hidden");
    departmentSelect.disabled = true;
    courseSelect.disabled = true;
  } else if (role === "admin") {
    // Show department selection for admins
    departmentSelect.classList.remove("hidden");
    courseSelect.classList.add("hidden");
    departmentSelect.disabled = false;
    courseSelect.disabled = true;
  } else if (role === "moderator") {
    // Show department and course selection for moderators
    departmentSelect.classList.remove("hidden");
    courseSelect.classList.remove("hidden");
    if (requestUserDepartment != "-1") {
      departmentSelect.disabled = true;
    } else {
      departmentSelect.disabled = false;
    }
    courseSelect.disabled = false;
  }
}

// Save Assignment Function
function saveAssignment() {
  const role = document.getElementById("roleSelect").value;

  let departmentId = document.getElementById("departmentIdHidden").value; // Get the department ID from the hidden field
  if (!departmentId) {
    departmentSelect = document.getElementById("departmentSelect");
    departmentId = departmentSelect.value;
  }
  const courseSelect = document.getElementById("courseSelect");

  // Get departmentId directly, even if the dropdown is locked or disabled
  const courseId = courseSelect.value;

  // Log the values for debugging purposes
  console.log("Saving assignment for user:", selectedUserId);
  console.log(
    "Role:",
    role,
    "DepartmentId:",
    departmentId,
    "CourseId:",
    courseId
  );

  // Logic to save the role assignment (send data to the server via AJAX)
  const data = {
    user_id: selectedUserId,
    appoint_role: role, // Send the role being assigned
    department_id: departmentId, // Always send department_id, even if the dropdown is locked
    course_id: courseId, // Include course_id in data
    institute_id: userInstituteId, // Send institute_id if needed
  };
  console.log(data);

  // Send only department_id or course_id based on the selected role
  if (role === "admin") {
    // Only send department_id for Admin (do not send course_id)
    delete data.course_id;
  }

  // Debug log the data object being sent
  console.log("Data being sent to the server:", data);

  // Send data to the server for processing
  fetch("/appoint_user/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.text()) // Read response as text first
    .then((responseText) => {
      console.log("Full response text:", responseText); // Log the raw response
      try {
        const result = JSON.parse(responseText); // Try parsing JSON
        console.log("Role assignment saved successfully:", result);
        window.location.href = "/appoint";
        closeAppointModal();
      } catch (error) {
        console.error("Error parsing JSON:", error);
        console.log("Response text is not valid JSON:", responseText);
      }
    })
    .catch((error) => {
      console.error("Error assigning role:", error);
    });
}
