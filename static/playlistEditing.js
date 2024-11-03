const chosenMusicInput = document.getElementById("chosenMusicPieces");

// Function to handle the click event for each music row button
function handleButtonClick(event) {
    const button = event.currentTarget;
    const row = button.closest(".music-row");
    const svg = button.querySelector("svg");
    const rowId = row.getAttribute("data-id");

    // Determine if the music row is currently in the Available or Added section
    const isAvailable = svg.classList.contains("plus-icon");

    if (isAvailable) {
        // Move to Added Music section
        document.querySelector(".pieces-in-playlist").appendChild(row);
        playlistValues.push(parseInt(rowId));

        // Update icon to trash icon
        button.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6 trash-icon">
  <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
</svg>`;
        svg.classList.remove("plus-icon");
        svg.classList.add("trash-icon");
    } else {
        // Move back to Available Music section
        document.querySelector(".Available-music").appendChild(row);
        const index = playlistValues.indexOf(parseInt(rowId));
        if (index > -1) {
            playlistValues.splice(index, 1);
        }

        // Update icon to plus icon
        button.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-6 plus-icon">
                  <path fill-rule="evenodd" d="M12 3.75a.75.75 0 0 1 .75.75v6.75h6.75a.75.75 0 0 1 0 1.5h-6.75v6.75a.75.75 0 0 1-1.5 0v-6.75H4.5a.75.75 0 0 1 0-1.5h6.75V4.5a.75.75 0 0 1 .75-.75Z" clip-rule="evenodd"></path>
               </svg>`;
        svg.classList.remove("trash-icon");
        svg.classList.add("plus-icon");
    }

    // Update the hidden input field
    chosenMusicInput.value = playlistValues.join(",");
    console.log("Chosen pieces:", playlistValues); // Optional: log to verify
}

// Attach the event listener to each music row button
document.querySelectorAll(".music-row-piece-button button").forEach(button => {
    button.addEventListener("click", handleButtonClick);
});

function updateHiddenInput() {
    // Update the hidden input with the current values in playlistValues
    chosenMusicInput.value = playlistValues.join(",");
    console.log("Form submission - Chosen Music Pieces:", chosenMusicInput.value); // For debugging
}

function previewImage(event) {
    const imagePreview = document.getElementById('imagePreview');
    const placeholderText = document.getElementById('placeholderText');

    if (event.target.files && event.target.files[0]) {
        // Display the new image
        const reader = new FileReader();
        reader.onload = function(e) {
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'block';
            placeholderText.style.display = 'none';
        };
        reader.readAsDataURL(event.target.files[0]);
    }
}

// Function to toggle the "No music available to select" message
function toggleNoMusicMessage() {
    const availableMusicDiv = document.querySelector('.Available-music');
    const noMusicMessage = document.getElementById('noMusicMessage');

    // Check if there are any music items in the Available-music div
    const hasMusicItems = availableMusicDiv.querySelectorAll('.music-row').length > 0;

    // Show or hide the message based on the presence of music items
    noMusicMessage.style.display = hasMusicItems ? 'none' : 'block';
}

// Function to add music back to the available section and update the message
function addMusicToAvailable(musicItem) {
    const availableMusicDiv = document.querySelector('.Available-music');
    availableMusicDiv.appendChild(musicItem);
    toggleNoMusicMessage(); // Update message visibility
}

// Function to remove music from the available section and update the message
function removeMusicFromAvailable(musicItem) {
    musicItem.remove();
    toggleNoMusicMessage(); // Update message visibility
}

// Initial call to set the message visibility when the page loads
toggleNoMusicMessage();

