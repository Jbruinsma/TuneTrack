// Show the modal
function showModal() {
    document.getElementById("confirmModal").classList.remove("hidden");
}

// Close the modal
function closeModal() {
    document.getElementById("confirmModal").classList.add("hidden");
}

function confirmDeletion(playlistId) {
    fetch(`/delete_playlist/${playlistId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ playlist_id: playlistId })
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/';
        } else {
            console.error('Failed to delete playlist.');
        }
    })
    .catch(error => console.error('Error:', error));

    closeModal();
}

// Close modal when clicking outside of it
window.onclick = function (event) {
    const modal = document.getElementById("confirmModal");
    if (event.target === modal) {
        closeModal();
    }
};
