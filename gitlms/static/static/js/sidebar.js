function toggleSidebar() {
  let sidebar = document.getElementById("sidebar");
  let sidebarButton = document.getElementById("sideBarButton");
  let content = document.getElementById("content");

  // Toggle sidebar open/close
  sidebar.classList.toggle("open");
  sidebarButton.classList.toggle("hidden");
  // Toggle main content margin-left to shift
  content.classList.toggle("shifted");
}

// Check screen size on page load and set the sidebar's initial state
window.addEventListener("load", function () {
  let sidebar = document.getElementById("sidebar");
  let content = document.getElementById("content");

  if (window.innerWidth < 768) {
    // On smaller screens, remove the "open" class and reset the content's margin
    sidebar.classList.remove("open");
    content.classList.remove("shifted");
  } else {
    // On larger screens, apply the "open" class to keep the sidebar open
    sidebar.classList.add("open");
    content.classList.add("shifted");
  }
});

// Check the screen size on resize
window.addEventListener("resize", function () {
  let sidebar = document.getElementById("sidebar");
  let content = document.getElementById("content");

  if (window.innerWidth < 768) {
    // On smaller screens, remove the "open" class and reset the content's margin
    sidebar.classList.remove("open");
    content.classList.remove("shifted");
  } else {
    // On larger screens, apply the "open" class to keep the sidebar open
    sidebar.classList.add("open");
    content.classList.add("shifted");
  }
});
