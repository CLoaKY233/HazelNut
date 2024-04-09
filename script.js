// Get references to elements
const announcementForm = document.getElementById('announcement-form');
const sidePanel = document.getElementById('sidePanel');
const sidePanelItems = document.querySelectorAll('.side-panel li');
const contentSections = document.querySelectorAll('.content');
const toggleButton = document.getElementById('toggleSidePanel');

// Function to handle content switching
function switchContent(contentId) {
  contentSections.forEach(section => {
    section.classList.remove('active');
  });
  document.getElementById(contentId).classList.add('active');
}

// Event listener for form submission
announcementForm.addEventListener('submit', (event) => {
  event.preventDefault(); // Prevent default form submission behavior

  // Replace this with your actual logic to process the announcement (e.g., send data to server)
  console.log('Announcement submitted:', announcementForm.elements);

  // Clear form fields after submission
  announcementForm.reset();
});

// Function to toggle side panel visibility
function toggleSidePanel() {
  sidePanel.classList.toggle('collapsed');
}

// Add event listener to toggle button
toggleButton.addEventListener('click', toggleSidePanel);

// Add event listeners to side panel items for content switching
sidePanelItems.forEach(item => {
  item.addEventListener('click', () => {
    // Collapse the side panel when a menu item is clicked
    sidePanel.classList.add('collapsed');

    // Remove active class from all side panel items
    sidePanelItems.forEach(item => {
      item.classList.remove('active');
    });

    // Add active class to the clicked item
    item.classList.add('active');

    // Get the corresponding content id and switch content
    const contentId = item.getAttribute('data-content');
    switchContent(contentId);
  });
});
