function updateMoodTags() {
    const moodSlider = document.getElementById('mood');
    const moodTagsContainer = document.getElementById('moodTagsCheckboxes');
    const moodScoreDisplay = document.getElementById('moodScore');
  
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
      label.className='tag-label'
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
  
