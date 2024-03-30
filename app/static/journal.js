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

function deleteEntry(entryId) {
  fetch('/delete-entry', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': '{{ csrf_token() }}'  // Include CSRF token for security
      },
      body: JSON.stringify({ entryId: entryId })
  })
  .then(response => {
      if (response.ok) {
          window.location.reload();
      } else {
          console.error('Failed to delete entry');
      }
  })
  .catch(error => {
      console.error('Error deleting entry:', error);
  });
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
// Function to create meal entry
function createMealEntry() {
  const mealName = document.getElementById('mealName').value;
  const mealDescription = document.getElementById('mealDescription').value;
  
  // Check if both mealName and mealDescription are not empty
  if (mealName && mealDescription) {
    const mealEntry = document.createElement('div');
    mealEntry.textContent = mealName + ' - ' + mealDescription;
    document.getElementById('mealContainer').appendChild(mealEntry);
    
    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'X';
    deleteButton.addEventListener('click', function() {
      mealEntry.remove();
    });
    mealEntry.appendChild(deleteButton);
  } else {
    alert('Both meal name and description are required.');
  }
}
// Event listener for "Add Meal" button
document.getElementById('addMealButton').addEventListener('click', function() {
  createMealEntry();
});

// Function to create sleep time entry
function createSleepTimeEntry() {
  const sleepStartTime = document.getElementById('sleepStartTime').value;
  const sleepEndTime = document.getElementById('sleepEndTime').value;
  
  // Check if both sleepStartTime and sleepEndTime are not empty
  if (sleepStartTime && sleepEndTime) {
    const sleepEntry = document.createElement('div');
    sleepEntry.textContent = sleepStartTime + ' - ' + sleepEndTime;
    document.getElementById('sleepTimesContainer').appendChild(sleepEntry);
    
    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'X';
    deleteButton.addEventListener('click', function() {
      sleepEntry.remove();
    });
    sleepEntry.appendChild(deleteButton);
  } else {
    alert('Both sleep start and end times are required.');
  }
}

// Event listener for "Add Sleep Time" button
document.getElementById('addSleepButton').addEventListener('click', function() {
  createSleepTimeEntry();
});

// Event listener for "Add Food" button
document.getElementById('foodButton').addEventListener('click', function() {
  document.getElementById('foodForm').style.display = 'block';
  document.getElementById('sleepForm').style.display = 'none';
});

// Event listener for "Add Sleep" button
document.getElementById('sleepButton').addEventListener('click', function() {
  document.getElementById('sleepForm').style.display = 'block';
  document.getElementById('foodForm').style.display = 'none';
});

function toggleDetails(event) {
  // Find the entry-details-container related to the clicked arrow button
  var entryDetailsContainer = event.target.parentElement.nextElementSibling;
  
  // Toggle the display of the entry-details-container
  if (entryDetailsContainer.style.display === "none") {
      entryDetailsContainer.style.display = "block";
      event.target.textContent = "▼"; // Change the arrow to point down
  } else {
      entryDetailsContainer.style.display = "none";
      event.target.textContent = "◄"; // Change the arrow to point left
  }
}





