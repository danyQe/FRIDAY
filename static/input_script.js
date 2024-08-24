        document.addEventListener('DOMContentLoaded', function () {
            const voicewave = document.getElementById("bars");
            const closeButton = document.getElementById('close-button');
            const microphone = document.getElementById('microphone');
            const textBox = document.getElementById('text-box');
            const textButton = document.getElementById('text-button');
            const recognition = new webkitSpeechRecognition(); // Stop Web Speech API recognition
            const uploadButton=document.getElementById("upload-button");
            const pdf_file= document.getElementById("pdf-container");
            let isListening = false;
            let initialActive = true;
            let active = false;
            let mic=false;
            let isvoiceinputactive=true;
            let request=false;
            // const chatbox = document.getElementById('chatbox');
            textButton.disabled = true;
            textButton.style.backgroundColor = 'gray';
            function checkInternetConnection() {
                 return navigator.onLine;
             }
            function hideMicrophoneButton() {
                const microphoneButton = document.getElementById('microphone');
                microphoneButton.style.display = 'none';
                microphone.style.display = 'none'; // Hide the microphone button
                voicewave.style.display = 'flex'; // Show the voice wave container
                closeButton.style.display = 'block'; // Show the close button
            }
            
            function showMicrophoneButton() {
                const microphoneButton = document.getElementById('microphone');
                microphoneButton.style.display = 'inline-block';
                closeButton.style.display = 'none'; // Hide the close button
                microphone.style.display = 'block'; // Show the microphone button
                voicewave.style.display = 'none'; // Hide the voice wave container // Adjust display property as needed
            }
            
            function speak(text,callback) {
                text = text.replace(/\*/g, '');
            const voices = speechSynthesis.getVoices();
            // const languages=navigator.languages;
            // const languagecode=languages[0];
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.voice = voices[2]; // Choose a specific voice
            try {
        speechSynthesis.speak(utterance);
        utterance.onend = function() {
            if(!isListening){
            if (typeof callback === 'function') {
                callback();
            }
        }
        };
    } catch (error) {
        console.error('Error occurred during speech synthesis:', error);
        // Handle the error gracefully, such as displaying a message to the user
    }
}
            function voiceInput() {
                if(!isListening){
                    recognition.continuous = true;
                    recognition.interimResults = false;
                    recognition.lang = 'en-IN';
                    let wakeWord = "wake up friday";
                    let sleepWord = 'stop listening';
                    let inactiveTimeout = 600000; // 10 minutes in milliseconds
                    let lastActiveTime = Date.now();
                    let restartafterror=false;
                   
                    recognition.onresult = function (event) {
                        const text = event.results[0][0].transcript.toLowerCase();
                        if(!isvoiceinputactive)
                        {
                            recognition.stop();
                            return;
                        }
                        if (initialActive) {
                            initialActive = false;
                            lastActiveTime = Date.now();
                            active = true;
                            console.log("You said: " + text);
                            sendvoiceMessage(text);
                        }else{

                        let currentTime = Date.now();

                        // Check if inactive for 10 minutes
                        if (currentTime - lastActiveTime >= inactiveTimeout) {
                            console.log("Inactive for 10 minutes. Sleeping...'say wake up friday' to start ");
                            appendMessage("Inactive for ten minutes sleeping 'say wake up friday' to start ");
                            active = false;
                        }

                        if (text.includes(sleepWord) && active) {
                            console.log("Sleeping...");
                            appendMessage('Friday',"sleeping...'say wake up friday' to start '");
                            stopListening();
                            speak("ok stopped listening.....");
                            initialActive = false;
                        }
                        else if (text.includes(wakeWord) && !active) {
                            console.log("Waking up...");
                            lastActiveTime = Date.now();
                            hideMicrophoneButton();
                            active = true;
                            console.log("You said: " + text);
                            sendvoiceMessage(text);
                        }
                        else if(active)
                        {

                            console.log("sending text to server",text);
                            sendvoiceMessage(text);
                        }
                    }
            
                };
                    recognition.onerror = function (event) {
                        console.error("Error recognizing audio:", event.error);
                        isListening=false;
                        restartafterror=true;
    switch (event.error) {
        case 'no-speech':
            console.log('No speech detected');
            break;
        case 'aborted':
            console.log('Recognition aborted');
            break;
        case 'audio-capture':
            console.log('Audio capture error');
            break;
        case 'network':
            console.log('Network error');
            break;
        case 'not-allowed':
            console.log('Microphone access not allowed');
            break;
            case 'service-not-allowed':
                console.log('Speech recognition service not allowed');
                break;
                case 'bad-grammar':
                    console.log('Speech grammar error');
                    break;
                    default:
                        console.log('Unknown error');
                    }
                    if(restartafterror)
                    {
                        isListening=true;
                        recognition.stop();
                        startListening();
                    }
                };
                // recognition.onend=function()
                // {
                //   isListening=false;
                //   showMicrophoneButton();
                // };
               
                recognition.start();
                
                recognition.onstart=function()
                {
                    isListening=true;
                    hideMicrophoneButton();
                }
              }
            }

            function stopListening() {
                
                console.log('Stoped listening...');
                if (isListening) {
                   recognition.stop();
                  }
                showMicrophoneButton();
                isListening = false;
            }

            function startListening() {
                if (!isListening) { // Only start recognition if it's not already running
                hideMicrophoneButton();
                // isListening=true;
                voiceInput();
                 }
                console.log('Started listening...');
                textButton.disabled = true; // Disable the text button while listening
            }
            function sendvoiceMessage(message) {
                isvoiceinputactive=false;
                if(checkInternetConnection())
                {
                    textButton.disabled = true;
                textButton.style.backgroundColor = 'gray';
                appendMessage('user',message);
                stopListening();
                request=true;
                fetch('/send_message', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            message: message
                        })
                    })
                    .

then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        if (data.message) {
                            console.log('Response from backend', data.message);
                            isvoiceinputactive=true;
                            request=false;
                            processMessage(data.message);
                        } else {
                            console.error('Error: Response from backend is missing message');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        speak('errot occured:'+error,startListening);
                        isvoiceinputactive=true;
                    });
                }
                else{
                    alert("check your internet connection")
                }
            }
            function sendMessage(message) {
                if(checkInternetConnection())
                {
                    textButton.disabled = true;
                    request=true;
                textButton.style.backgroundColor = 'gray';
                appendMessage('user',message);

                fetch('/send_message', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            message: message
                        })
                    })
                    .

then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        if (data.message) {
                            // if (data.type==='code') {
                            //     appendCode(data.message);
                            // }
                            // console.log('Response from backend', data.message);
                            // appendMessage('Friday', data.message);
                            // speak(data.message);
                            processMessage(data.message);
                            request=false;
                        } else {
                            console.error('Error: Response from backend is missing message');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
                }
                else
                {
                    alert("check your internet connection or try again later.")
                }
            }

            function fetchSystemMessageFromBackend() {
                if(checkInternetConnection())
                {
                    fetch('/send_system_message', {
                        method: 'POST'
                    })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        const systemMessage = data.message;
                        console.log('Received system message from backend:', systemMessage);
                        // Process the received system message as needed
                        appendMessage('Friday', systemMessage);
                        speak(systemMessage);
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        // Handle error conditions
                    });
                }
                else{
                    alert("check your internet connection or try again later.")
                }
                }
            function  send_file()
            {
                
                const fileInput = document.getElementById('file-input');
                const upload = document.getElementById('upload');
                upload.addEventListener('click', function () {
                    pdf_file.style.display='none';
                    const file = fileInput.files[0];
                    if (!file) {
                        alert('Please select a file');
                        return;
                    }
                    appendMessage("Friday","summarizing "+file.name);
                    if (!file.name.endsWith('.pdf')) {
                        alert('Only PDF files are allowed to upload');
                        return;
                    }
    
                    const formData = new FormData();
                    formData.append('file', file);
     
                    fetch('/upload', {
                        method: 'POST',
                        body: formData,
                        // headers: {
                            // 'Content-Type': 'application/json'
                        // }
                    })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        if (data.message) {
                            // if (data.type==='code') {
                            //     appendCode(data.message);
                            // }
                            // console.log('Response from backend', data.message);
                            // appendMessage('Friday', data.message);
                            // speak(data.message);
                            processMessage(data.message);
                            request=false;
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('An error occurred while uploading the file');
                    });
                });
            }
                send_file();
                fetchSystemMessageFromBackend();
                function processMessage(message) {
                    const codePattern = /```(\w+)(.*?)```/gs; // Regex pattern to match code blocks
                    const wordPattern = /\*\*([\w\s]+)\*\*/g; // Regex pattern to match words enclosed in double asterisks
                    let codeMatch, wordMatch;
                    let startIndex = 0;
                
                    while ((codeMatch = codePattern.exec(message)) !== null || (wordMatch = wordPattern.exec(message)) !== null) {
                        // Append any text before the code block or word
                        if (codeMatch && codeMatch.index > startIndex) {
                            const textBeforeCode = message.substring(startIndex, codeMatch.index);
                            appendMessage('FRIDAY', textBeforeCode);
                            // const textBeforeCodeTrimmed = textBeforeCode.replace(/\*/g, ''); // Remove asterisks
                            // if(mic)
                            //  { speak(textBeforeCodeTrimmed);
                            //  }
                            //  else
                            //  {
                            //     speak(textBeforeCodeTrimmed);
                            //  }
                            startIndex = codeMatch.index + codeMatch[0].length;
                        } else if (wordMatch && wordMatch.index > startIndex) {
                            const textBeforeWord = message.substring(startIndex, wordMatch.index);
                            appendMessage('FRIDAY', textBeforeWord);
                            // if(mic)
                            //  { speak(textBeforeWord);
                            //  }
                            //  else
                            //  {
                            //     speak(textBeforeWord);
                            //  }
                            startIndex = wordMatch.index;
                        }
                
                        // Append the code block or word
                        if (codeMatch) {
                            const language = codeMatch[1];
                            const code = codeMatch[2].trim();
                            appendCode(code, language);
                            startIndex = codeMatch.index + codeMatch[0].length;
                        } else if (wordMatch) {
                            const word = wordMatch[1];
                            appendWordWithHeading(word);
                            // speak(word);
                            startIndex = wordMatch.index + wordMatch[0].length;
                        }
                    }
                
                    // Append any remaining text after the last code block or word
                    if (startIndex < message.length) {
                        const remainingText = message.substring(startIndex);
                        appendMessage('FRIDAY', remainingText);
                    //     if(mic)
                    //     {
                    //     speak(remainingText.replace(/\*/g, ''),startListening); 
                    //     }
                    //     else
                    //     {
                    //         speak(remainingText.replace(/\*/g, ''));// Remove asterisks
                    // }
                }
                if(mic)
                {
                    speak(message,startListening);
                }
                else
                {
                    speak(message);
                }
            }

            function appendCode(code,language) {
                const chatbox = document.getElementById('chatbox');
                const language_type=document.createElement('h2');
                const codeElement = document.createElement('code');
                language_type.id='language';
                codeElement.className='codeText';
                language_type.innerText=language;
                codeElement.innerText = code;
                const preElement = document.createElement('pre');
                preElement.appendChild(codeElement);
                chatbox.appendChild(language_type);
                chatbox.appendChild(preElement);
            }

            function appendMessage(sender, message) {
                $('#chatbox').css('display', 'block');
                $('#microphone-container-full').css('justify-content','flex-end');
                const chatbox = document.getElementById('chatbox');
                const messageElement = document.createElement('p');
                messageElement.innerText = message;
                messageElement.className = sender === 'user' ? 'userText' : 'botText';
                chatbox.appendChild(messageElement);
                // After appending a new message, scroll to the bottom to keep the latest messages visible
                chatbox.scrollTop = chatbox.scrollHeight;
            }
            function appendWordWithHeading(word) {
                const chatbox = document.getElementById('chatbox');
                const headingElement = document.createElement('h2');
                headingElement.innerText = word; // Set the heading text to the matched word
                chatbox.appendChild(headingElement);
            }
            

            let flag=false;
            uploadButton.addEventListener('click',function(){
               if(!flag)
               {
                flag=true;
               pdf_file.style.display='flex';
               }
               else{
                flag=false;
                pdf_file.style.display='none';
               }
            });
            // Add an input event listener to the text box
            textBox.addEventListener('input', function () {
                // Check if the text box is empty
                if (textBox.value.trim() === '') {
                    // If it's empty, disable the text button and change its background color to gray
                    textButton.disabled = true;
                    if(mic)
                    {
                        mic=false;
                        stopListening();
                    }
                    textButton.style.backgroundColor = 'gray';
                } else {
                    // If there is text, enable the text button and set its background color to green
                    textButton.disabled = false;
                    textButton.style.backgroundColor = 'rgb(49, 246, 15)'; // Green color
                }
            });
            textBox.addEventListener('keypress', function (event) {
                if (event.key === 'Enter') {
                    const message = textBox.value.trim();
                    if(navigator.onLine)
                    {
                        if(!request)
                          sendMessage(message);
                        else
                           alert("wait server is responding....");
                    }
                    else
                    {
                        alert("please check you internet connection");
                    }
                    // adjustSizes();
                    textBox.value = '';
                }
            });
            textButton.addEventListener('click', function () {
                const message = textBox.value.trim();
                if (message !== '') {
                    // Send text message to backend
                    if(navigator.onLine)
                    {
                        if(!request)
                        sendMessage(message);
                      else
                         alert("wait server is responding....");
                    }
                    else
                    {
                        alert("please check you internet connection");
                    }
                    //adjustSizes();
                    textBox.value = '';
                }
            });
            microphone.addEventListener('click', function () {
                console.log('Microphone clicked');
                if(!request)
                {mic=true;
                startListening();
                }
                else{
                    alert("wait server is responding....");
                } // Start listening to the microphone
            });

            closeButton.addEventListener('click', function () {
                console.log('Close button clicked');
                mic=false;
                stopListening(); // Stop listening to the microphon
            });

            document.getElementById('restart-button').addEventListener('click', function () {
                fetch('/restart_backend', {
                        method: 'POST'
                    })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        if (data.message) {
                            processMessage(data.message);
                        } else {
                            console.error('Error: Response from backend is missing message');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
            });
        });
