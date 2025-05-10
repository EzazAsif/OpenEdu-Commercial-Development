function toggleMenu(menuId) {
    document.querySelectorAll('.menu-dropdown').forEach(menu => {
      if (menu.id !== menuId) {
        menu.classList.add('hidden');
      }
    });
    document.getElementById(menuId).classList.toggle('hidden');
  }

  // Close menu when clicking outside
  document.addEventListener('click', function(event) {
    let menus = document.querySelectorAll('.menu-dropdown');
    menus.forEach(menu => {
      if (!menu.contains(event.target) && !event.target.closest('button')) {
        menu.classList.add('hidden');
      }
    });
  });