const backButton = document.querySelector('.bl')
const PPButton = document.getElementById('customPausePlayButton')
const nextButton = document.querySelector('.br')
const audioPlayer = document.getElementById('audioPlayer');
const volumeSlider = document.getElementById('volumeSlider');
const id = playlistId

const wpTitle = document.querySelector('title')
const image = document.querySelector('.playlist-image')
const title = document.querySelector('.details h3')
const artist = document.querySelector('.details p')

const shuffleBtn = document.querySelector('.shuffle-piece button')
const loopBtn = document.querySelector('.loop-piece button')
const loopBtnContainer = document.querySelector('.loop-piece')
const shuffleBtnContainer = document.querySelector('.shuffle-piece')

let tempValueList = [];

function placeholder() {
    console.log('This function is a placeholder. Fix if getting an error.')
}

function togglePlayPause() {
    const PPButton = document.getElementById('customPausePlayButton');
    const currentState = PPButton.getAttribute('data-state');

    if (currentState === 'pause') {
        audioPlayer.play();
        PPButton.innerHTML = `
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 5.25v13.5m-7.5-13.5v13.5" />
</svg>`;
        PPButton.setAttribute('data-state', 'play');
    } else {
        audioPlayer.pause();
        PPButton.innerHTML = `
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
  <path stroke-linecap="round" stroke-linejoin="round" d="M5.25 5.653c0-.856.917-1.398 1.667-.986l11.54 6.347a1.125 1.125 0 0 1 0 1.972l-11.54 6.347a1.125 1.125 0 0 1-1.667-.986V5.653Z" />
</svg>

        `;
        PPButton.setAttribute('data-state', 'pause');
    }
}

function sliderInput() {
    const currentTime = audioPlayer.currentTime;
    const duration = audioElement.duration;

    if (!isNaN(duration)) {
        slider.max = duration;
        slider.value = currentTime;
    }
}

function seekAudio() {
    audioElement.currentTime = slider.value;
}

function volumeInput() {
    audioElement.volume = volumeSlider.value;
}

function reset() {
    slider.value = 0;
}

function display_data(data, operation) {

    const receivedData = data;

    function manageCounter(cur_value, len) {
        let count_value = cur_value;

        if (operation === 'starting') {
            tempValueList = [];
            return count_value;
        } else if (operation === 'next') {
            if (cur_value === len) {
                return 0;
            } else {
                count_value += 1;
                return count_value;
            }
        } else {
            if (count_value === 0) {
                return 0;
            } else {
                count_value -= 1;
                return count_value;
            }
        }
    }

    function updateValueList() {
        let counter = 1;
        while (playlistValues.indexOf(counter) === -1) {
            tempValueList.push(counter);
            counter += 1;
        }
        return tempValueList;
    }

    async function addTempList() {
        let updatedValueList = '';

        try {
            const response = await fetch('/api/update_value_list', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({tempValueList}),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            updatedValueList = await response.json();
        } catch (error) {
            console.error('Error:', error);
        }

        return getUpdatedValueList();
    }

    function getUpdatedValueList() {
        return fetch('/api/get/value_list')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
    }

    const currentlyPlaying = receivedData[0];
    let playlistValues = receivedData[1];

    const currentState = PPButton.getAttribute('data-state');
    const imagePath = `/static/albumCovers/${currentlyPlaying['image']}`;
    const audioPath = `/static/audio/${currentlyPlaying['path']}`;

    playlistValueCounter = manageCounter(playlistValueCounter, playlistValues.length - 1);
    console.log(`Counter: ${playlistValueCounter}`)

    if (playlistValueCounter === 0 && firstLoad !== true) {
        let newPlaylistValues = updateValueList();
        playlistValues = newPlaylistValues.concat(playlistValues);
    }

    musicPieceId = playlistValues[playlistValueCounter];

    console.log(`Piece ID: ${musicPieceId}`)

    wpTitle.textContent = `Now Playing: ${currentlyPlaying['music_name']}`;
    image.src = `${imagePath}`;
    title.textContent = `${currentlyPlaying['music_name']}`;
    artist.textContent = `${currentlyPlaying['artist']}`;


    audioSource.src = `${audioPath}`;
    audioElement.load();


    if (firstLoad === true) {
        audioElement.volume = 0;
        volumeSlider.value = 0;
        firstLoad = false;
    }

    if (currentState === 'play') {
        audioElement.play().catch(function (error) {
            console.error('Playback failed:', error);
        });
    } else {
        audioElement.pause()
    }

    if (playlistValueCounter === 0 && firstLoad !== true) {
        playlistValues = addTempList();
    }
}

function fetchStartingPlay() {
    return fetch(`/api/get/${id}`)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
        display_data(data, 'starting')
      return data;
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });
}

function fetchStartingSpecific(){
    return fetch(`/api/get_specific/${startingIndex}/${playlistId}`)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      // Process the data here
        display_data(data)
      return data;
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });
}

function fetchStartingShuffle(){
    return fetch(`/api/get_shuffle/-1/${playlistId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Process the data here
            display_data(data)
            return data;
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}
function fetchNext() {

        return fetch(`/api/next`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Process the data here
                reset()
                display_data(data, 'next')
                return data
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
}

function fetchPrev() {
    return fetch(`/api/prev`)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      // Process the data here
        reset()
        display_data(data, 'prev')
      return data;
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });
}

function checkForLoop() {
    reset()
    if (loopBtnContainer.classList.contains('active')) {
        console.log('looping')
        audioElement.play();
    } else {
        fetchNext()
    }
}

function loopBtnCheck() {
    checkIfActive(loopBtnContainer)
}

function shuffleBtnCheck() {
    if (checkIfActive(shuffleBtnContainer) === true) {

        return fetch(`/api/shuffle_from/${musicPieceId}/${playlistId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Process the data here
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });

    } else {
        console.log('undoing shuffle')

        return fetch(`/api/unshuffle_playlist/${musicPieceId}/${playlistId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Process the data here
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });

    }
}

function checkIfActive(btn){
    if (btn.classList.contains('active')) {
    btn.classList.remove('active')
        return false
    } else {
        btn.classList.add('active')
        return true
    }
}

function checkAction() {

    function tryConvertToInt(startingIndex) {
        let parsedIndex = parseInt(startingIndex, 10);
        if (isNaN(parsedIndex)) {
            return false;
        } else {
            return parsedIndex;
        }
    }

    if (tryConvertToInt(startingIndex) === false) {
        shuffleBtnContainer.classList.add('active')
        console.log('shuffle is working')
        fetchStartingShuffle()
    } else {
        if (startingIndex === '0') {
            fetchStartingPlay();
        } else {
            fetchStartingSpecific()
        }
    }
}

document.addEventListener('DOMContentLoaded', checkAction)
backButton.addEventListener("click", fetchPrev)
nextButton.addEventListener("click", fetchNext)
shuffleBtn.addEventListener('click', shuffleBtnCheck)
loopBtn.addEventListener('click', loopBtnCheck)
PPButton.addEventListener('click', togglePlayPause)

audioPlayer.addEventListener('ended', checkForLoop)
volumeSlider.addEventListener('input', volumeInput)

audioElement.addEventListener('timeupdate', sliderInput);
slider.addEventListener('input', seekAudio);