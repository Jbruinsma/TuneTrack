document.addEventListener("DOMContentLoaded", function () {
    const audioPlayer = document.getElementById("audioPlayer");
    const volumeSlider = document.getElementById("volumeSlider");

    // Set the initial volume to 0 (muted)
    audioPlayer.volume = 0;

    // Update the audio player's volume as the user adjusts the slider
    volumeSlider.addEventListener("input", function () {
        audioPlayer.volume = volumeSlider.value;
    });

    // Other slider functions (progress bar, etc.) can remain unchanged
    const playButton = document.getElementById("customPlayButton");
    const progressBar = document.getElementById("progressBar");

    // Play/Pause functionality
    playButton.addEventListener("click", function () {
      if (audioPlayer.paused) {
        audioPlayer.play();
        playButton.innerHTML = "<svg xmlns=\"http://www.w3.org/2000/svg\" fill=\"none\" viewBox=\"0 0 24 24\" stroke-width=\"1.5\" stroke=\"currentColor\" class=\"size-6\">\n" +
            "  <path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M15.75 5.25v13.5m-7.5-13.5v13.5\" />\n" +
            "</svg>\n"; // Change button text
      } else {
        audioPlayer.pause();
        playButton.innerHTML = "<svg xmlns=\"http://www.w3.org/2000/svg\" fill=\"none\" viewBox=\"0 0 24 24\" stroke-width=\"1.5\" stroke=\"currentColor\" class=\"size-6\">\n" +
            "  <path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5.25 5.653c0-.856.917-1.398 1.667-.986l11.54 6.347a1.125 1.125 0 0 1 0 1.972l-11.54 6.347a1.125 1.125 0 0 1-1.667-.986V5.653Z\" />\n" +
            "</svg>\n";
      }
    });

    // Update the progress bar as the audio plays
    audioPlayer.addEventListener("timeupdate", function () {
      progressBar.max = audioPlayer.duration;
      progressBar.value = audioPlayer.currentTime;
    });

    // Seek functionality
    progressBar.addEventListener("input", function () {
      audioPlayer.currentTime = progressBar.value;
    });
});
