$(document).ready(function() {
    // Your animation code here
    // $( ". selector" ). loader( "hide" ); 
    var words = ["Hello there!","I am Rolex","Your personalised voice assistant"],
        part,
        i = 0,
        offset = 0,
        len = words.length,
        forwards = true,
        skip_count = 0,
        skip_delay = 10,
        speed = 50;

    var wordflick = function() {
        setInterval(function() {
            if (forwards) {
                if (offset >= words[i].length) {
                    ++skip_count;
                    if (skip_count == skip_delay) {
                        forwards = false;
                        skip_count = 0;
                    }
                }
            } else {
                if (offset == 0) {
                    forwards = true;
                    i++;
                    offset = 0;
                    if (i >= len) {
                        i = 0;
                    }
                }
            }
            part = words[i].substr(0, offset);
            if (skip_count == 0) {
                if (forwards) {
                    offset++;
                } else {
                    offset--;
                }
            }
            $('.word').text(part);
        }, speed);
    };

    // Call the wordflick function here
    wordflick();

    // Check internet connection and show popup on start button click
    $('#start-button').on('click', async function() {
        const isConnected = await checkInternetConnection();
        document.getElementById("loader").style.display = "grid";
        if (isConnected) {
            document.getElementById("loader").style.display = "none";
            showpopup();
        } else {
            document.getElementById("loader").style.display = "none";
            alert('Internet connection is not available. Please connect to the internet.');
        }
    });
    $('#save_api_button').on('click', async function() {
         saveAPIKeys();                 
    });

    // Function to check internet connection
    function checkInternetConnection() {
        return fetch('https://www.google.com', { mode: 'no-cors' })
            .then(response => {
                if (response.ok || response.type === 'opaque') {
                    console.log('Internet is available');
                    return true;
                } else {
                    console.log('Internet is not available');
                    return false;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                console.log('Internet is not available');
                return false;
            });
    }
    
    // Function to show popup
    function showpopup() {
        $('#popup').css('display', 'block');
    }
    function showapikeyPopup() {
        $('#popup').css('display', 'none');
        document.getElementById("apiKeyPopup").style.display = "block";
    }

    // Function to hide the pop-up box
    function hidePopup() {
        document.getElementById("apiKeyPopup").style.display = "none";
        document.getElementById("loader").style.display = "grid";
    }

    // Function to save API keys
    function saveAPIKeys() {
        const googleApiKey = document.getElementById("googleApiKey").value;
        
        const requestData = {
            google_api_key: googleApiKey
        };
    
        fetch('/save_keys', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // API keys saved successfully, hide the pop-up box
                hidePopup();
                window.location.href = window.location.href+'/input';
            } else {
                console.error('Failed to save API keys');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
    
    // Function to check if API keys are present
    function checkKeys() {
        fetch('/check_keys')
            .then(response => response.json())
            .then(data => {
                if (!data.keys_present) {
                    // API keys are missing, show the pop-up box
                    document.getElementById("loader").style.display = "none";
                    showapikeyPopup();
                }
                else
                {
                    $('#popup').css('display', 'none');
                    document.getElementById("loader").style.display = "grid";
                    window.location.href = window.location.href+'input';
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
    function checkKeys_without_camera() {
        fetch('/check_keys')
            .then(response => response.json())
            .then(data => {
                if (!data.keys_present) {
                    // API keys are missing, show the pop-up box
                    document.getElementById("loader").style.display = "none";
                    showapikeyPopup();
                }
                else
                {
                    $('#popup').css('display', 'none');
                    document.getElementById("loader").style.display = "grid";
                    window.location.href = window.location.href+'input';
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
    // Call the function to check if API keys are present when the page is loaded
    // Close popup when close button is clicked
    $('#closePopup').on('click', function() {
        $('#popup').css('display', 'none');
    });
     
    // Redirect to the next page when confirm button is clicked
    $('#confirmButton').on('click', function() {
        document.getElementById("loader").style.display = "grid";
        checkKeys();
    });
    $('#disagreeButton').on('click',function()
    {
        document.getElementById('loader').style.display="grid";
        checkKeys_without_camera();
    })
});