function updateMoodTags() {
  const moodSlider = document.getElementById('mood');
  const moodTagsContainer = document.getElementById('moodTagsCheckboxes');
  const moodScoreDisplay = document.getElementById('moodScore');

  // Check if the container element exists
  if (!moodTagsContainer) {
    console.error("Mood tags container not found.");
    return;
  }

  // Clear existing checkboxes
  moodTagsContainer.innerHTML = '';

  // Determine mood value
  const moodValue = moodSlider.value;

  // Update mood score display
  moodScoreDisplay.textContent = `${moodValue}/10`;

  // Determine mood tags based on the mood value
  let moodTags;
  if (moodValue <= 2) {
    moodTags = ['Annoyed', 'Anxious', 'Disappointed', 'Empty', 'Frustrated', 'Guilty', 'Hopeless', 'Lonely', 'Nervous', 'Overwhelmed', 'Sad', 'Stressed', 'Tired', 'Worried'];
  } else if (moodValue <= 4) {
    moodTags = ['Upset', 'Confused', 'Restless', 'Uneasy', 'Frustrated', 'Disturbed', 'Unsettled', 'Lonely', 'Nervous', 'Overwhelmed', 'Sad', 'Mild', 'Tired', 'Worried'];
  } else if (moodValue <= 6) {
    moodTags = ['Neutral', 'Calm', 'Composed', 'Content', 'Appeased', 'Fulfilled', 'Relieved', 'Grateful', 'Inspired', 'Peaceful', 'Confident', 'Hopeful', 'Sunny', 'Eager'];
  } else if (moodValue <= 8) {
    moodTags = ['Joyful', 'Calm', 'Composed', 'Content', 'Appeased', 'Fulfilled', 'Relieved', 'Grateful', 'Cheerful', 'Upbeat', 'Confident', 'Hopeful', 'Motivated', 'Eager'];
  } else {
    moodTags = ['Joyful', 'Ecstatic', 'Thrilled', 'Euphoric', 'Energized', 'Happy', 'Fulfilled', 'Excited', 'Cheerful', 'Upbeat', 'Confident', 'Hopeful', 'Motivated', 'Eager'];
  }

  // Add new checkboxes to the container
  moodTags.forEach(tag => {
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.name = 'moodTags';
    checkbox.value = tag.toLowerCase();
    checkbox.id = tag.toLowerCase();

    const label = document.createElement('label');
    label.htmlFor = tag.toLowerCase();
    label.className = 'tag-label';
    label.textContent = tag;

    const container = document.createElement('div');
    container.className = 'mood-tag';

    container.appendChild(checkbox);
    container.appendChild(label);
    moodTagsContainer.appendChild(container);
  });
}

// Call the function on page load
document.addEventListener('DOMContentLoaded', updateMoodTags);

// deletes entries
function deleteEntry(entryId) {
  console.log(`Deleting entry with ID: ${entryId}`);
  fetch("/delete-entry", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ entryId: entryId }),
  })
  .then((_res) => {
    console.log("Entry deleted successfully");
    window.location.href = "/journal";
  })
  .catch(error => console.error('Error deleting entry:', error));
}

function deleteEvent(eventId) {
  console.log(`Deleting event with ID: ${eventId}`);
  fetch("/delete-event", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",  // Set the correct content type
    },
    body: JSON.stringify({ eventId: eventId }),
  })
  .then(response => response.json())
  .then(data => {
    if (data.error) {
      throw new Error(data.error);
    }
    console.log("Event deleted successfully");
    window.location.href = "/schedule";
  })
  .catch(error => {
    console.error('Error deleting event:', error.message);
    // Handle the error gracefully, e.g., show a user-friendly message
  });
}

// JavaScript functions for dropdown functionality
function toggleDropdown() {
  document.getElementById("iconDropdown").classList.toggle("show");
}

function selectIcon(iconClass) {
  document.getElementById("selectedIcon").className = "fa " + iconClass;
  document.getElementById("selectedIconValue").value = iconClass;
  toggleDropdown(); // Close the dropdown after selecting an icon
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.custom-dropdown')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      for (var i = 0; i < dropdowns.length; i++) {
          var openDropdown = dropdowns[i];
          if (openDropdown.classList.contains('show')) {
              openDropdown.classList.remove('show');
          }
      }
  }
};


