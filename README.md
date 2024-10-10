# **🧠 Friday: Advanced AI Voice Assistant**  
[![Version](https://img.shields.io/badge/version-1.0-brightgreen.svg)]() [![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)]() [![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)]() [![License](https://img.shields.io/badge/license-MIT-yellow.svg)]()  

**Friday** is your personal AI assistant, designed to streamline your day by offering seamless interaction with multiple services. It responds to your mood, performs system-level tasks, automates scripts, and even handles everyday activities like music playback, coding, and messaging.

> **Live Demo**: 🔴 *Coming Soon*

---

## 🎉 **Key Features**  

✨ **Emotion Recognition**  
The assistant reads your facial emotions in real-time using advanced computer vision techniques and responds according to your mood—whether you're feeling happy, sad, or neutral. Your assistant understands you!  

🌐 **Web Scraping**  
Need quick answers? Friday can browse the web and fetch the most accurate information for you.  

🎶 **Media Control**  
Easily control your favorite media apps. Say "Play [song] on Spotify" or "Play [video] on YouTube," and Friday will do the rest.  

💻 Program Writing and Execution
Friday can write and execute programs in Python, allowing you to automate tasks or perform computations with simple commands. For example, you can say, "Write a program to calculate the factorial of a number."

📲 **WhatsApp Messaging**  
Send WhatsApp messages to any of your contacts by simply saying, "Send a WhatsApp message to [contact]."  

💻 **PyAutoGUI Script Generation**  
Friday can automate your tasks by writing and executing **PyAutoGUI** scripts, controlling your system with commands like mouse movements, clicks, and keyboard inputs.  

📜 **User History Tracking**  
The assistant stores a log of your actions and interactions to personalize your experience. The next time you chat, it remembers your preferences!  

🛠️ **System Commands**  
Commands like “Shut down,” “Restart,” “Sleep,” and setting alarms make Friday your ultimate assistant for controlling system functions.  

📝 **PDF Summarization**  
Need a quick summary of a long PDF? Friday can summarize documents for you within seconds.  

---

## 🌟 **Screenshots**  
Here's a sneak peek of the UI:

## UI Preview
![Home Screen](/screenshots/homescreen.png)  
*The main interface of Friday, showcasing the home screen.*

![Input Screen](/screenshots/input_screen.png)  
*The input screen where users can interact with Friday via text or voice commands.*
---

## 🚀 **Getting Started**  

### **Prerequisites**  
Ensure the following are installed before starting the project:  

- Python 3.7+
- Flask  
- OpenCV (for emotion recognition)
- deepface(for emotion , age and gender recognition)
- PyAutoGUI (for automation)  
- SpeechRecognition 
- Pyttsx3
- json
- dotenv
- youtube_transcript_api
- BeautifulSoup
- PYPDF2
- googletrans
- screen_brightness_control
- seleneium
- PIL
- Requests (for gemini LLM API data retrieval)
Install dependencies with:  
```bash
pip install -r requirements.txt
```
---

## 💻 **Running the Project**  

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/danyQe/FRIDAY.git
   cd FRIDAY
   ```

2. **Start the Flask Server**  
   ```bash
   python app.py
   ```
---

## 🛠️ **How It Works**  

### **Emotion Recognition**  
Your webcam captures your face, and using **OpenCV** and **deepface**, it detects your facial expressions(age,gender,emotion). The assistant analyzes your mood and responds accordingly.  

### **Web Scraping & Media Control**  
Friday uses **Selenium** and the **Beautiful soup** to fetch data and summarise the results based on your input. 
Spotify app is must in the windows pc to play the songs.

### **Code Execution**  
Through **PyAutoGUI**, the assistant can write and execute Python scripts for system control, such as automating mouse clicks or typing tasks.  

### **Interaction History**  
Each conversation is logged in a text file for later reference, allowing the assistant to better understand and tailor future interactions.  

### **Summarisation**
 The Friday can summarise the pdf's as well as youtube video's 
---

## 📂 **Project Structure**  
```bash
FRIDAY/
│
├── app.py                  # Main Flask server
├── gemini_functions.py     # API keys and configuration
├── prompt.py               # the prompts used to control the gemini model
├── .env                    # the API keys will be stored here.
├── history.txt             # the data of the user will be stored here.
├── messages.json           # the json schema between user and the model will be stored here.these data can be used to fine tune the model further.
├── /static                 # Static files (CSS, JS, images)
├── /templates              # HTML templates for UI
├── /programs               # The generated programms will be stored here.
├── /photos                 # The user's face database to save their names with photos.
├── /documents              # The pdf documents will be stored here for summarisation.
└── requirements.txt        # Project dependencies
```

---

## 🤖 **How to Use Friday**  


### **1. For Web Scraping & Information:**  
Ask anything:  
```
"Find the latest news about AI"  
"What's the weather like today?"  
```

### **2. For Media Control:**  
```
"Play [song name] on Spotify"  
"Play [video name] on YouTube"  
```

### **3. For Sending WhatsApp Messages:**  
```
"Send a WhatsApp message to [contact] saying [message]"  
```

### **4. For Code Execution (PyAutoGUI):**  
```
"Write a script to click the mouse at [x, y] position."  
"Automate typing this sentence."  
```

### **5. System Commands:**  
```
"Shut down the system."  
"Restart the system."  
"Set an alarm for 7 AM."  
```

---

## 🔧 **Contributing**  

We welcome contributions! Feel free to fork the repository and submit pull requests for new features or bug fixes. If you're unsure how to contribute, check out our [contribution guidelines](CONTRIBUTING.md).

---

## 📜 **License**  
This project is licensed under the MIT License.
---

## 📬 **Contact**  

For any inquiries, feel free to reach out via email: raogoutham374@gmail.com

---

Hope this README inspires you to use Friday and build upon it. Contributions and feedback are always appreciated!

---

This version should capture attention with some cool formatting and icons, making it more engaging for users. Feel free to add screenshots, GIFs, or even links to live demos for added flair.
