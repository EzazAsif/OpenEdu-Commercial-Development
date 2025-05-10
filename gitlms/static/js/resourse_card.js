document.addEventListener('DOMContentLoaded', function() {
    const dropdownButtons = document.querySelectorAll('.dropdown > button');
    
    dropdownButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            const menu = this.nextElementSibling;
            const isHidden = menu.classList.contains('hidden');
            
            // Close all other menus
            document.querySelectorAll('.dropdown-menu').forEach(m => {
                if (m !== menu) m.classList.add('hidden');
            });
            
            // Toggle this menu
            menu.classList.toggle('hidden', !isHidden);
        });
    });
    
    // Close menus when clicking elsewhere
    document.addEventListener('click', function() {
        document.querySelectorAll('.dropdown-menu').forEach(menu => {
            menu.classList.add('hidden');
        });
    });
    
    // Add click handlers for update/delete buttons (example functionality)
    document.querySelectorAll('.dropdown-menu button').forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            const action = this.textContent.trim();
            const cardTitle = this.closest('.p-5').querySelector('h3').textContent;
            alert(`${action} action clicked for ${cardTitle}`);
        });
    });
});