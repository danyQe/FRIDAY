document.addEventListener('DOMContentLoaded', function () {
    // DOM Elements
    const chatbox = document.getElementById('chatbox');
    const voicewave = document.getElementById("voice-wave");
    const stopButton = document.getElementById('stop-button');
    const microphone = document.getElementById('microphone');
    const textBox = document.getElementById('text-box');
    const textButton = document.getElementById('text-button');
    const uploadButton = document.getElementById("upload-button");
    const pdfFile = document.getElementById("pdf-container");
    const fileInput = document.getElementById('file-input');
    const voiceSelect = document.getElementById('voice-select');
    const speechToggle = document.getElementById('speech-toggle');
    
    
    // State variables
    let isListening = false;
    let isSpeaking = true; // Controls whether ROLEX speaks
    let currentConversation = false;
    let request = false;

    // Initialize speech recognition
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.continuous = true;
    recognition.interimResults = false;
    recognition.lang = 'en-IN';

    // Disable text button initially
    textButton.disabled = true;
    textButton.style.backgroundColor = 'gray';
    function populateVoiceSelect() {
        const voices = speechSynthesis.getVoices();
        voiceSelect.innerHTML = voices
            .map((voice, index) => `<option value="${index}">${voice.name}</option>`)
            .join('');
    }

    // Handle voice loading
    if (speechSynthesis.onvoiceschanged !== undefined) {
        speechSynthesis.onvoiceschanged = populateVoiceSelect;
    }

    // Voice Wave Animation
    function startVoiceWaveAnimation() {
        voicewave.style.display = 'flex';
        const bars = voicewave.children;
        for (let bar of bars) {
            const height = Math.random() * 40 + 10;
            bar.style.height = `${height}px`;
        }
        requestAnimationFrame(startVoiceWaveAnimation);
    }
    // Utility Functions
    function checkInternetConnection() {
        return navigator.onLine;
    }

    function hideMicrophoneButton() {
        microphone.style.display = 'none';
        voicewave.style.display = 'flex';
        closeButton.style.display = 'block';
    }

    function showMicrophoneButton() {
        microphone.style.display = 'block';
        closeButton.style.display = 'none';
        voicewave.style.display = 'none';
    }

    // Speech Synthesis
    function speak(text, callback) {
        if (!isSpeaking) {
            if (callback) callback();
            return;
        }

        text = text.replace(/\*/g, '');
        const voices = speechSynthesis.getVoices();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.voice = voices[voiceSelect.value];

        try {
            speechSynthesis.speak(utterance);
            utterance.onend = function() {
                if (currentConversation && typeof callback === 'function') {
                    callback();
                }
            };
        } catch (error) {
            console.error('Error during speech synthesis:', error);
            if (callback) callback();
        }
    }

    function startConversation() {
        if (!currentConversation) {
            currentConversation = true;
            microphone.style.display = 'none';
            stopButton.style.display = 'block';
            voicewave.style.display = 'flex';
            startVoiceWaveAnimation();
            recognition.start();
        }
    }

    // Stop Conversation
    function stopConversation() {
        currentConversation = false;
        recognition.stop();
        speechSynthesis.cancel();
        microphone.style.display = 'block';
        stopButton.style.display = 'none';
        voicewave.style.display = 'none';
    }
    recognition.onresult = function(event) {
        const text = event.results[event.results.length - 1][0].transcript;
        if (currentConversation) {
            sendVoiceMessage(text);
        }
    };

    recognition.onend = function() {
        if (currentConversation) {
            recognition.start();
        }
    };
    // Voice Input Processing
    function voiceInput() {
        if (!isListening) {
            const wakeWord = "wake up friday";
            const sleepWord = 'stop listening';
            const inactiveTimeout = 600000;
            let lastActiveTime = Date.now();
            let restartAfterError = false;

            recognition.onresult = function(event) {
                const text = event.results[0][0].transcript.toLowerCase();
                
                if (!isVoiceInputActive) {
                    recognition.stop();
                    return;
                }

                if (initialActive) {
                    initialActive = false;
                    lastActiveTime = Date.now();
                    active = true;
                    sendVoiceMessage(text);
                } else {
                    let currentTime = Date.now();

                    if (currentTime - lastActiveTime >= inactiveTimeout) {
                        appendMessage("Friday", "Inactive for ten minutes sleeping 'say wake up friday' to start ");
                        active = false;
                    }

                    if (text.includes(sleepWord) && active) {
                        appendMessage('Friday', "sleeping...'say wake up friday' to start '");
                        stopListening();
                        speak("ok stopped listening.....");
                        initialActive = false;
                    } else if (text.includes(wakeWord) && !active) {
                        lastActiveTime = Date.now();
                        hideMicrophoneButton();
                        active = true;
                        sendVoiceMessage(text);
                    } else if (active) {
                        sendVoiceMessage(text);
                    }
                }
            };

            recognition.onerror = function(event) {
                console.error("Speech recognition error:", event.error);
                isListening = false;
                restartAfterError = true;
                
                if (restartAfterError) {
                    isListening = true;
                    recognition.stop();
                    startListening();
                }
            };

            recognition.onstart = function() {
                isListening = true;
                hideMicrophoneButton();
            };

            recognition.start();
        }
    }

    // Message Processing
    function processMessage(message) {
        const codePattern = /```(\w+)(.*?)```/gs;
        const wordPattern = /\*\*([\w\s]+)\*\*/g;
        let codeMatch, wordMatch;
        let startIndex = 0;

        while ((codeMatch = codePattern.exec(message)) !== null || (wordMatch = wordPattern.exec(message)) !== null) {
            if (codeMatch && codeMatch.index > startIndex) {
                const textBeforeCode = message.substring(startIndex, codeMatch.index);
                appendMessage('FRIDAY', textBeforeCode);
                startIndex = codeMatch.index + codeMatch[0].length;
            } else if (wordMatch && wordMatch.index > startIndex) {
                const textBeforeWord = message.substring(startIndex, wordMatch.index);
                appendMessage('FRIDAY', textBeforeWord);
                startIndex = wordMatch.index;
            }

            if (codeMatch) {
                const language = codeMatch[1];
                const code = codeMatch[2].trim();
                appendCode(code, language);
                startIndex = codeMatch.index + codeMatch[0].length;
            } else if (wordMatch) {
                const word = wordMatch[1];
                appendWordWithHeading(word);
                startIndex = wordMatch.index + wordMatch[0].length;
            }
        }

        if (startIndex < message.length) {
            const remainingText = message.substring(startIndex);
            appendMessage('FRIDAY', remainingText);
        }

        if (mic) {
            speak(message, startListening);
        } else {
            speak(message);
        }
    }

    // Message Display Functions
    function appendCode(code, language) {
        const languageType = document.createElement('h2');
        const codeElement = document.createElement('code');
        languageType.id = 'language';
        codeElement.className = 'codeText';
        languageType.innerText = language;
        codeElement.innerText = code;
        const preElement = document.createElement('pre');
        preElement.appendChild(codeElement);
        chatbox.appendChild(languageType);
        chatbox.appendChild(preElement);
    }

    function appendMessage(sender, message) {
        $('#chatbox').css('display', 'block');
        $('#microphone-container-full').css('justify-content', 'flex-end');
        const messageElement = document.createElement('p');
        messageElement.innerText = message;
        messageElement.className = sender === 'user' ? 'userText' : 'botText';
        chatbox.appendChild(messageElement);
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    function appendWordWithHeading(word) {
        const headingElement = document.createElement('h2');
        headingElement.innerText = word;
        chatbox.appendChild(headingElement);
    }

    // API Communication Functions
    // function sendVoiceMessage(message) {
    //     isVoiceInputActive = false;
    //     if (checkInternetConnection()) {
    //         textButton.disabled = true;
    //         textButton.style.backgroundColor = 'gray';
    //         appendMessage('user', message);
    //         stopListening();
    //         request = true;

    //         fetch('/send_message', {
    //             method: 'POST',
    //             headers: { 'Content-Type': 'application/json' },
    //             body: JSON.stringify({ message: message })
    //         })
    //         .then(response => {
    //             if (!response.ok) throw new Error('Network response was not ok');
    //             return response.json();
    //         })
    //         .then(data => {
    //             if (data.message) {
    //                 isVoiceInputActive = true;
    //                 request = false;
    //                 processMessage(data.message);
    //             }
    //         })
    //         .catch(error => {
    //             console.error('Error:', error);
    //             speak('error occurred:' + error, startListening);
    //             isVoiceInputActive = true;
    //         });
    //     } else {
    //         alert("Check your internet connection");
    //     }
    // }
    async function sendVoiceMessage(message) {
        if (!navigator.onLine) {
            alert("Check your internet connection");
            return;
        }

        appendMessage('user', message);
        request = true;

        try {
            const response = await fetch('/send_message', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });

            if (!response.ok) throw new Error('Network response was not ok');
            
            const data = await response.json();
            if (data.message) {
                processMessage(data.message);
                request = false;
            }
        } catch (error) {
            console.error('Error:', error);
            speak('An error occurred while processing your request');
            request = false;
        }
    }

    function sendMessage(message) {
        if (checkInternetConnection()) {
            textButton.disabled = true;
            request = true;
            textButton.style.backgroundColor = 'gray';
            appendMessage('user', message);

            fetch('/send_message', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            })
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(data => {
                if (data.message) {
                    processMessage(data.message);
                    request = false;
                }
            })
            .catch(error => console.error('Error:', error));
        } else {
            alert("Check your internet connection or try again later.");
        }
    }

    // File Upload Handler
    function handleFileUpload() {
        const file = fileInput.files[0];
        if (!file) {
            alert('Please select a file');
            return;
        }

        pdfFile.style.display = 'none';
        appendMessage("Friday", "summarizing " + file.name);

        if (!file.name.endsWith('.pdf')) {
            alert('Only PDF files are allowed to upload');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            if (data.message) {
                processMessage(data.message);
                request = false;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while uploading the file');
        });
    }

    // Event Listeners
    uploadButton.addEventListener('click', () => {
        flag = !flag;
        pdfFile.style.display = flag ? 'flex' : 'none';
    });

    textBox.addEventListener('input', () => {
        const isEmpty = textBox.value.trim() === '';
        textButton.disabled = isEmpty;
        if (mic && isEmpty) {
            mic = false;
            stopListening();
        }
        textButton.style.backgroundColor = isEmpty ? 'rgb(105, 229, 229)' : 'rgb(9, 122, 234)';
    });

    textBox.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            const message = textBox.value.trim();
            if (checkInternetConnection()) {
                if (!request) {
                    sendMessage(message);
                } else {
                    alert("Wait server is responding....");
                }
            } else {
                alert("Please check your internet connection");
            }
            textBox.value = '';
        }
    });

    textButton.addEventListener('click', () => {
        const message = textBox.value.trim();
        if (message && checkInternetConnection()) {
            if (!request) {
                sendMessage(message);
            } else {
                alert("Wait server is responding....");
            }
            textBox.value = '';
        }
    });

    microphone.addEventListener('click', startConversation);
    stopButton.addEventListener('click', stopConversation);
    
    speechToggle.addEventListener('change', function() {
        isSpeaking = this.checked;
    });

    // Handle file uploads
    uploadButton.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', handleFileUpload);
    document.getElementById('upload').addEventListener('click', handleFileUpload);

    // Voice Control Functions
    function startListening() {
        if (!isListening) {
            hideMicrophoneButton();
            voiceInput();
        }
        textButton.disabled = true;
    }

    function stopListening() {
        if (isListening) {
            recognition.stop();
        }
        showMicrophoneButton();
        isListening = false;
    }
});