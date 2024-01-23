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
  