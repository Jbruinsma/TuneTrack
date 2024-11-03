const playlistImageInput = document.getElementById("playlistImage");
const imagePreview = document.getElementById("imagePreview");
const placeholderText = document.querySelector('.upload-placeholder');
const uploadIcon = document.querySelector('.upload-icon');
const availableMusic = document.querySelectorAll(".music-row");
const chosenMusicInput = document.getElementById("chosenMusicPieces"); // Hidden input for selected pieces


const chosen_music_pieces = []

playlistImageInput.addEventListener("change", function(event) {
    if (event.target.files && event.target.files[0]) {
        const reader = new FileReader();

        reader.onload = function(e) {
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'block';
            placeholderText.style.display = 'none';
            uploadIcon.style.display = 'none';
        };

        reader.readAsDataURL(event.target.files[0]);
    }
});

availableMusic.forEach(row => {
    const button = row.querySelector("button");
    const svg = button.querySelector("svg");
    const rowId = row.getAttribute("data-id");

    button.addEventListener("click", () => {
        const piecesInPlaylist = document.querySelector(".pieces-in-playlist");

        if (svg.classList.contains("plus-icon")) {
            // Move row to playlist and update icon to the new trash icon
            piecesInPlaylist.appendChild(row);
            chosen_music_pieces.push(rowId);

            button.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6 trash-icon">
  <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
</svg>`;
            svg.classList.remove("plus-icon");
            svg.classList.add("trash-icon");
        } else {
            // Move row back to available music and update icon to plus icon
            document.querySelector(".Available-music").appendChild(row);
            const index = chosen_music_pieces.indexOf(rowId);
            if (index > -1) {
                chosen_music_pieces.splice(index, 1);
            }

            button.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-6 plus-icon">
                  <path fill-rule="evenodd" d="M12 3.75a.75.75 0 0 1 .75.75v6.75h6.75a.75.75 0 0 1 0 1.5h-6.75v6.75a.75.75 0 0 1-1.5 0v-6.75H4.5a.75.75 0 0 1 0-1.5h6.75V4.5a.75.75 0 0 1 .75-.75Z" clip-rule="evenodd"></path>
               </svg>`;
            svg.classList.remove("trash-icon");
            svg.classList.add("plus-icon");
        }

        chosenMusicInput.value = chosen_music_pieces.join(",");
        console.log("Chosen pieces:", chosen_music_pieces); // Optional: log to verify
    });
});