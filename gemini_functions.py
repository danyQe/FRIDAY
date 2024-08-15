import os
import pyttsx3
import speech_recognition as sr
import pyautogui
import time
import requests
from PIL import Image
import subprocess
import PyPDF2
from selenium import webdriver
import win32gui
import datetime
from googletrans import Translator 
from  PIL import Image,ImageTk
import psutil
# from deepface import DeepFace
from pathlib import Path
# import screen_brightness_control as sbc 
import cv2
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
# from selenium.webdriver.common.by import By
import requests
from dotenv import load_dotenv
import os
from youtube_transcript_api import YouTubeTranscriptApi
import subprocess
from os import system, listdir
from bs4 import BeautifulSoup
load_dotenv()
api_key=os.getenv("GOOGLE_API_KEY")
os.getenv("TF_ENABLE_ONEDNN_OPTS")
headers = {
    'Content-Type': 'application/json'
      }
#the functions used internally 
def fix_content(text):
   try:
    text = text.replace("\\n", "\n")
    text = text.replace("\\\"", "\"")
    text = text.replace("|n|", "\n")
    text = text.replace("\\" , "")
    return text
   except:
       return text
def count_tokens(message):
    try:
        messages={
            "role":"user",
            "parts": [{"text":message}]
        }
        data1={
                "contents":[messages]
            }
        count_tokens_response=requests.post("https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:countTokens?key="+api_key,json=data1,headers=headers)
        count_token=count_tokens_response.json()
        print(count_token)
        total_tokens=count_token.get('totalTokens')
        print(total_tokens)
        return total_tokens
    except Exception as e:
        print(f"exception occured in counting tokens in gemini function{e}")
        return 0
def summarize_content(messages,prompt=None):
    try:
         if prompt:
            prompt=f"generate a summary of the whole content the instructions you follow to summarize this content as follows:{prompt} and the content is :{messages}"
            message={
             "role":"user",
             "parts": [{"text":prompt}]
            }
         else:
            prompt=f"generate a summary of the whole content remove uneccessary text and unneccessary links but keep the important links which can help me to research further.generate the content in the points format.If the text has some code ,you have to show the exact code in it. the content must be atmost 10000 words the content is {messages} ."
            message={
             "role":"user",
             "parts": [{"text":prompt}]
            }
         data={
             "contents":[message]
         }
         response= requests.post("https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" +api_key, json=data,headers=headers)
         if(response.status_code==200):
             response=response.json()
             if "candidates" not in response:
                 return f"unable to summarize the  content:{messages}"
             message = response['candidates'][0]['content']['parts'][0]['text']
             message=fix_content(message)
             return message
         elif(response.status_code==500):
              return "internal server error occured please try later."
         else:
             return f"unable to summarize the content check your internet connection or try again later.the reason is{response.text}"
    except Exception as e:
        return f"Error occured in summarizing :{e}.The unsummarized content is :{message}"
def extract_text(html_content):
    try:
        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        # Extract all text from the HTML
        all_text = soup.get_text(separator='\n')
        return all_text
    except Exception as e:
        print(f"exception occured when extracting text from html content:{e}")
        return f"unable to extract the text from web html content{html_content} using beautiful soup."
def extract_links(html_content):
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        all_links = soup.find_all("a")
 # Extract the href attribute from each <a> tag
        links = [link.get("href") for link in all_links]
        links = [link for link in links if link]
        return links
    except Exception as e:
        print(f"exception occured while extracting links from webcontent:{e}")
        return "no links are there"
def speak(output):
    engine = pyttsx3.init()
    voices=engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(output)
    engine.runAndWait()

def get_voice_input():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Say something...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text.lower()

    except sr.UnknownValueError as e:
        print(f"Error recognizing audio: {e}")
        return get_voice_input()
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return get_voice_input()
def open_image():
    # Open the image using PIL
    window=tk.Tk()
    window.title("Image Viewer")
    image_path=os.listdir('output')[-1:]
    image = Image.open(image_path)

    # Convert the image to a format compatible with Tkinter
    tk_image = ImageTk.PhotoImage(image)

    # Create a Tkinter label widget to display the image
    label = tk.Label(window, image=tk_image)
    label.image = tk_image  # Keep a reference to avoid garbage collection

    # Pack the label widget into the window
    label.pack()
    window.mainloop()


#the user functions called by gemini
def web_scrape(url):
    # Launch Microsoft Edge with Selenium
    # driver = webdriver.Edge()
    try:
        #  options = EdgeOptions()
        #  options.add_experimental_option('excludeSwitches', ['enable-logging'])
         driver = webdriver.Edge()
     
         # Navigate to the specified URL
         driver.get(url)
     
         html_content=driver.page_source
     
         # Close the browser
         driver.quit()
         all_text=extract_text(html_content)
         print(all_text)
         all_links=extract_links(html_content)
         all_text=f"Text:{all_text},Links:{all_links}"
         if(count_tokens(all_text)<30720):
             summarized_text=summarize_content(all_text)
             return f"{summarized_text}."
         else:
             return "the content in the page is larger than expected.please reduce it or  try again later."
    except Exception as e:
        print(f"unable to webscrape noe the error is{e}")
        return f"unable to webscrape noe the error is{e}"

def open_application(app_name):
    try:
         # Press Windows key to open Start menu
         pyautogui.press('win')
         time.sleep(1)  # Wait for the Start menu to open
         
         # Type the application name in the search box
         pyautogui.write(app_name, interval=0.1)  # Typing slowly for accuracy
         time.sleep(1)  # Wait for search results to appear
         
         # Press Enter to open the application
         pyautogui.press('enter')
         return "application opened successfully."
    except Exception as e:
        return f"error occured when opening application:{e}"
# def get_name(name=None):
#     if not name:
#         try:
#             current_brightness = sbc.get_brightness()
#             sbc.set_brightness(100)
#         except Exception as e:
#             print(f"Error: {e}") 
        
#         face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#         camera = cv2.VideoCapture(0)
        
#         if not camera.isOpened():
#             print("Error: Unable to access the camera.")
#             return "Error: Unable to access the camera."
        
#         cv2.namedWindow("Camera")
#         cv2.setWindowProperty("Camera", cv2.WND_PROP_TOPMOST,1.0)
#         start_time = time.time()
        
#         hold_message_time =4  # Time to display "Hold, don't move" message in seconds
#         timeout_time = 600  # Timeout in seconds (10 minutes)
        
#         while time.time() - start_time < timeout_time:
#             ret, image = camera.read()
            
#             if not ret:
#                 print("Error: Unable to capture photo.")
#                 break
            
#             cv2.imshow("Camera", image)
#             key = cv2.waitKey(1)
            
#             gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#             faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))
            
#             if len(faces) > 0:
#                 # Draw rectangle around detected face
#                 # Display "Hold, don't move" message for hold_message_time seconds
#                 for (x, y, w, h) in faces:
#                     cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)  
#                 cv2.imshow("Camera", image)
            
#                 # Wait for hold_message_time seconds before capturing photo
#                 if time.time() - start_time > hold_message_time:
#                     cv2.imwrite("cp.jpg", image  )
#                     time.sleep(3)  # Pause execution for 3 seconds
                    
#                     # Release camera and close window after image saved successfully
#                     camera.release()
#                     cv2.destroyAllWindows()
                    
#                     break  # Exit the loop after image saved successfully

#             else:
#                 # If no face detected, continue displaying camera feed
#                 continue
        
#         try:
#             sbc.set_brightness(current_brightness[0])
#         except Exception as e:
#             print(f"Error: {e}")
        
#         file_path = Path("photos/representations_vgg_face.pkl")
        
#         try:
#             file_path.unlink()
#             print(f"{file_path} has been deleted successfully.")
#         except OSError as e:
#             print(f"Error: {file_path}: {e.strerror}")
        
#         if len(faces) == 0:
#             print("Error: No face detected within the time limit.")
#             return "Error: No face detected within the time limit."
        
#         if not os.path.exists("photos"):
#             os.makedirs("photos")
        
#         photo_files = [f for f in os.listdir("photos") if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
#         if not photo_files:
#             print("Error: Unable to recognize the image.")
#             return "Error: Unable to recognize the image."
        
#         try:
#             result = DeepFace.find(img_path='./cp.jpg', db_path="photos", enforce_detection=False, threshold=0.3)
#             analysis = DeepFace.analyze(img_path='./cp.jpg', actions=['emotion', 'age'], enforce_detection=False)
#         except Exception as e:
#             print(f"Error: {e}")
#             return f"Error: {e}"
        
#         detected_age = analysis[0]['age'] - 4
#         detected_emotion = analysis[0]['dominant_emotion']
#         identity = str(result[0]['identity'])
        
#         print(f"Identity: {identity}")
        
#         if '_' in identity:
#             recognised_name = os.path.basename(identity).split('_')[0]
#             print(f"Recognised Name: {recognised_name}")
#         else:
#             recognised_name = os.path.basename(identity).split('.')[0] # Extract the name without extension
#             print(f"Recognised Name: {recognised_name}")
        
#         if len(result) > 0 and not result[0].empty:
#             user_name = os.path.basename(identity).split('.')[0]
#             print(f"Username: {user_name}")
            
#             image_name = f"{recognised_name}_{len(os.listdir('photos')) + 1}.jpg"
#             cv2.imwrite(os.path.join("photos", image_name), image)
#             print(f"Recognised Name: {recognised_name}, Emotion: {detected_emotion}, Age: {detected_age}")
            
#             if os.path.exists("cp.jpg"):
#                 os.remove("cp.jpg")
#                 print("cp.jpg has been deleted successfully.")
            
#             return f"Recognised Name: {recognised_name}, Emotion: {detected_emotion}, Age: {detected_age}"
#         else:
#             print(f"Error: Unable to recognize the face.please provide your name detected emotion:{detected_emotion},detected age :{detected_age}")
#             return f"Error: Unable to recognize the face.please provide your name detected emotion:{detected_emotion},detected age :{detected_age}"
        
#     elif name:
#         try:
#             analysis = DeepFace.analyze(img_path='cp.jpg', actions=['emotion', 'age'], enforce_detection=False)
#         except Exception as e:
#             print(f"Error: {e}")
#             return f"Error: {e}"
        
#         detected_emotion = analysis[0]['dominant_emotion']
#         detected_age = analysis[0]['age']
        
#         user_folder = 'photos'
#         image_name = f"{name}_{len(os.listdir(user_folder)) + 1}.jpg"
        
#         cv2.imwrite(os.path.join(user_folder, image_name), cv2.imread('cp.jpg'))
#         print(f"Recognised Name: {name} saved successfully, Emotion: {detected_emotion}, Age: {detected_age}")
        
#         if os.path.exists("cp.jpg"):
#             os.remove("cp.jpg")
#             print("cp.jpg has been deleted successfully.")
        
#         return f"Name: {name} saved successfully. Emotion: {detected_emotion}, Age: {detected_age}"
def get_date_and_time():
    try: 
        now = datetime.datetime.now()
        date_string = now.strftime("%Y-%m-%d")
        time_string = now.strftime("%I:%M:%S %p")
        return f"date:{date_string}, Time:{time_string}"
    except Exception as e:
        return "unable to find date and time"
def write_to_history_file(content):
    content = fix_content(content)  # Assuming fix_content is defined elsewhere
    filename = "history.txt"    
    try:
        with open(filename, "a",encoding='utf-8') as f:
            f.write(content + "\n")
        return {"status": f"Successfully written to file {filename}"}
    except OSError as e:
        return {"status": f"ERROR: Failed to write to file {filename}, {e}"}
def read_from_history_file():
    filename='history.txt'
    try:
        with open(filename, 'r',encoding='utf-8') as file:
             lst = [line.strip() for line in file]
        return lst
    except Exception :
        return f"cannot read the {filename}"
def translate_to_english(text):
  """Translates a text to English.

  Args:
    text: The text to translate.

  Returns:
    The translated text.
  """

  # Create a translator object
  translator = Translator()

  # Detect the language of the text
  language = translator.detect(text)
  # Translate the text to English
  translation = translator.translate(text, dest="en", src=language.lang)

  # Return the translated text
  return f"{translation.text},detected language code is :{language.lang}"
def translate_english_to_detected_language(text, language_code):
    try: 
          """Translates a text to the detected language.
        
          Args:
            text: The text to translate.
            language_code: The language code of the detected language.
        
          Returns:
            The translated text.
          """
          # Create a translator object
          translator = Translator()
        
          # Detect the language of the text
          language = translator.detect(text)
        
          # Translate the text to the detected language
          translation = translator.translate(text, dest=language_code, src=language.lang).pronunciation
        
          # Return the translated text
          return f"translated text:{translation}"
    except Exception as e:
         return f"error occured while translating to detected language:{e}"
    
def summarize_pdf(pdf_path,prompt=None):
    try:
        text = ""
        if not os.path.exists('documents'):
            # Create the directory if it doesn't exist
            os.makedirs('documents')
        full_pdf_path = os.path.join('documents', pdf_path)
        with open(full_pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                text += page.extract_text()
            print(text)
            if prompt:
               prompt=f"this is the content of the pdf . so summarize the content accordingly and don't miss any data. and the instructions maybe has some specific questions related to pdf follow these instructions or question and answer accordingly:{prompt}"
            else:   
               prompt="this is the content of the pdf . so summarize the content accordingly and don't miss any data.summarize it in points wise."
            if(count_tokens(text)<30720):
                summarized_text=summarize_content(text,prompt=prompt)
                return summarized_text
            else:
                return "the pdf  is larger than expected.please give small pdf's."
    except FileNotFoundError:
        return "PDF file not found"
    except Exception as e:
        return f"Error: {str(e)}"
def execute_python_code(python_code):
    try:
        # Write the provided Python code to a temporary file
        python_code=fix_content(python_code)
        with open("temp_code.py", "w") as file:
            file.write(python_code)

        # Define the command to execute the temporary Python file
        command = ["python", "temp_code.py"]

        # Execute the command
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Wait for the process to finish and get the return code
        return_code = process.wait()

        if return_code == 0:
            temp_path=Path("temp_code")
            return "Successfully executed"
        else:
            return "Failed to execute"

    except Exception as e:
        return f"Error: {e}"
def reminder(query=None):
    """%Y-%m-%d %H:%M"""
    if query is None:
        subprocess.Popen(["python","alarm.py"])
    else:
        subprocess.Popen(["python", "alarm.py", query])
def take_screen_shot():
    im = pyautogui.screenshot()
    im.save("ss.jpg")
    return f"saved as ss.jpg"
def generate_images(prompt):
    try:
        u_cookie_value=os.getenv('u_cookie_value')
        system(f'python -m BingImageCreator -U "{u_cookie_value}" --prompt "{prompt}"')
        output_dir='output'
        if not os.path.exists(output_dir):
        # Create the directory if it doesn't exist
            os.makedirs(output_dir)
        image_names=listdir("output")
        try:
            last_four_images=image_names[-4:]
            for image_name in last_four_images:
                image_path=os.path.join(output_dir,image_name)
                with Image.open(image_path) as img:
                    img.show()
        except Exception as e:
            print(f"error occured in opening Images:{e}")
        return f"images are stored in the output folder{image_names [-4:]}"
    except Exception as e:
        return f"exception found:{e}"
def play_music(song_name):
    """
    Opens Spotify and plays a song.

    Parameters:
        song_name (str): The name of the song to be played.

    Returns:
        bool: True if the song was successfully played, False otherwise.
    """
    # Press Windows key to open Start menu
    try:
        pyautogui.press('win')
        time.sleep(2)
    
        # Type "Spotify" to search for Spotify and press Enter
        pyautogui.write('Spotify')
        time.sleep(2)
        pyautogui.press('enter')
    
        program_name = "Spotify.exe"
        timeout_duration = 150  # Timeout duration in seconds
        start_time = time.time()
    
        # Wait until Spotify is open or timeout occurs
        while time.time() < start_time + timeout_duration:
            for process in psutil.process_iter():
                try:
                    if process.name() == program_name:
                        print("Spotify is open!")
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            else:
                time.sleep(1)
                continue
            break
        else:
            print("Timed out!")
            return False
    
        # Wait for Spotify to load
        time.sleep(20)
    
        # Focus on the Spotify window
        spotify_window = pyautogui.getWindowsWithTitle("Spotify")[0]
        spotify_window.maximize()
    
        # Focus on the search bar
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(3)
    
        # Type the song name in the search bar and press Enter
        pyautogui.write(song_name, interval=0.2)
        time.sleep(5)
        pyautogui.press('enter')
        time.sleep(1)
        # Select the first search result (assuming it's the desired song)
        for _ in range(3):  # Press Tab 6 times to navigate to the first search result
            pyautogui.press('tab')
            time.sleep(0.5)
        pyautogui.press('enter')
    
        # Check if the song started playing
        time.sleep(5)  # Wait for the song to start playing
        screenshot = pyautogui.screenshot(region=(935, 925, 49, 51))
        if "paused" not in pyautogui.screenshot(region=(935, 925, 49, 51)).tobytes().decode():
            print(f"Playing song: {song_name}")
            hwnd = win32gui.FindWindow(None, "Spotify Free")
            win32gui.ShowWindow(hwnd, win32gui.SW_MINIMIZE)
            return f"the song is playing:{song_name}"
        else:
            print(f"Failed to play song: {song_name}")
            return f"failed to play the song :{song_name}"
    except Exception as e:
        return f"unable to play the song{song_name} the error is:{e}"
def send_whatsapp_msg(receiver,msg):
    try:
       pyautogui.hotkey('win')
       time.sleep(3)
       pyautogui.write('whatsapp')
       time.sleep(7)
       pyautogui.press('enter')
       time.sleep(10)
       pyautogui.write(receiver,interval=0.2)
       pyautogui.hotkey('enter')
       time.sleep(8)
       pyautogui.press('tab')
       time.sleep(7)
       pyautogui.press('enter')
       time.sleep(2)
       pyautogui.write(msg,interval=0.3)
       time.sleep(7)
       pyautogui.hotkey('enter')
       time.sleep(10)
       pyautogui.hotkey('alt','f4')
    except Exception as e:
        speak("Sorry, I encountered an error in sending your message.")
        print(f"Error: {e}")
def write_program(language, code, file_name):
    """
    Writes a computer program to a file.

    Args:
        language: The language of the program.
        code: The code of the program.
        file_name: The name of the file to save the program to.
    Returns:
        The name of the file where the program was saved.
    """
    # Get the file extension for the given language.
    file_extension = {
        "python": ".py",
        "java": ".java",
        "c++": ".cpp",
        "javascript": ".js",  # Corrected language name
        "c": ".c",
        "sql": ".sql"
    }.get(language.lower())

    if file_extension is None:
        return print(f"Unsupported language: {language}")

    code = fix_content(code)

    # Add the file extension to the file name if it's not already there.
    if not file_name.endswith(file_extension):
        file_name += file_extension

    # Ensure that the directory exists, creating it if necessary.
    if not os.path.exists("programs"):
        os.makedirs("programs")

    # Write the code to the file.
    try:
        with open(os.path.join("programs", file_name), "w",encoding='utf-8') as f:
            f.write(code)
    except Exception as e:
        return print(f"Error writing to file: {e}")

    # Return the name of the file.
    return file_name
def read_program_file(file_name):
    """
    Reads a program file and returns the code.

    Args:
        file_name: The name of the file to read.

    Returns:
        The code in the file.
    """

    file_path = os.path.join("programs", file_name)

    try:
        with open(file_path, "r",encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        return print(f"File '{file_name}' not found")
    except Exception as e:
        return print(f"Error reading file '{file_name}': {e}")

    return code
def play_videos_on_youtube(video_name):
   try: 
       import pywhatkit
       pywhatkit.playonyt(video_name)
       return "successfully playing the youtube video."
   except Exception as e:
       return f"error occured while playing youtube video Error:{e}"
def summarise_the_youtube_video(video_url):
    try:
        video_id=video_url.split("=")[1]
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)
        transcript="this is the youtube video content so summarize the content accordingly content:"
        for i in transcript_text:
            transcript+=""+i["text"]
        transcript=summarize_content(transcript)
        return transcript
    except Exception as e:
        return f"error occured in transcripting.{e}"

#system commands called by gemini
def shutdown():
    try:
        speak("Do you really want to Shutdown this PC?")
        shutdown_response = get_voice_input().lower()
        if shutdown_response == 'yes':
            os.system("shutdown /s /t 1")
            return "shutdowning this pc."
        else:
             speak("ok sir stopped shutdowning")
             return "user said to stop shutdown."
    except Exception as e:
        return "error occured while shutdowning"
def restart():
    try:
        speak("The PC is restarting now.")
        time.sleep(2)
        speak("DO you really want to restart your pc")
        restart_response = get_voice_input().lower()
        if restart_response == 'yes':
            subprocess.call(["shutdown", "-r", "-t", "0"])
        else:
              return "user said stopped restarting."
    except Exception as e:
        return f"error ocuured while restarting:{e}"
def sleep():
    speak("The PC is going to sleep now.")
    time.sleep(3)
    os.system("Rundll32.exe Powrprof.dll,SetSuspendState 0,1,0")

function_definitions=[
    { "name":"web_scrape",
        "description":"this function is used to web scrape the links using selenium in python and the driver used here is microsoft edge",
        "parameters":
            {
                "type":"object",
                "properties":{
                    "url":
                        {
                         "type":"string",
                         "description":"this string is a url you need to scrap and read contents p element tags of the link."
                        }
                    }
            }
    },
    {"name":"open_application",
      "description":"this is the function to open an application using pyautogui .here using pyautogui you search the application.",
      "parameters":
          {
              "type":"object",
              "properties":{
                  "app_name":
                      {
                      "type":"string",
                      "description":"here is the application name."
                  }
              }
          }
     
     },
    # { "name":"get_name",
    #     "description":"this is the function which reads the face of the person and returns his name,emotion,age and gender .This function uses deepface model to recognise the emotion,age and gender.",
    #     "parameters":{
    #        "type":"object",
    #        "properties":
    #            {
    #                "name":
    #                    {
    #                        "type":"string",
    #                        "description":"this is the name attribute and this name attribute is optional .just provide name when it neccessary."
    #                    }
    #            }
    #     }
        
    # },
    {"name":"get_date_and_time",
        "description":"this is the function to extract the current date and time using datetime library in python"
    },
    {"name": "write_to_history_file",
        "description": "Writes content list  to a file .by using this function u can use it to store the history.you just have to provide content to write it in history file.the history file is already defined in this function",
        "parameters": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "Content to write to file .and this one is the history you want to write in a file to remember."
                }
            }
        }
    },
     {"name": "read_from_history_file",
        "description": "read content list  from a file .by using this function u can use it to retrieve the history."
    },
    {"name":"translate_to_english",
        "description":"this is the function used to translate the unidentified language text into english and the detected language code",
        "parameters":
            {
                "type":"object",
                "properties":{
                    "text":
                        {
                            "type":"string",
                            "description":"this is the text which is unidentified .you use it to translate the undetected text to english."
                        }
                }
            }
    },
    {"name":"translate_english_to_detected_language",
      "description":"this is the function which converts english to given language.you provide the language using language code",
      "parameters":{
          "type":"object",
          "properties":
              {
                  "text":
                      {
                          "type":"string",
                          "description":"this is the text which is converted from english language to given languiage code. "
                      },
                      "language_code":
                      {
                          "type":"string",
                          "description":"this is the language code you have to provide to the function .you get this language code from the translate_to_english_function."
                      }
              }
      }    
    }, 
    {"name":"summarize_pdf",
        "description":"it is a function to extract text from the pdf file using pypdf2 python library.",
        "parameters":
            {
                "type":"object",
                "properties":
                    {
                        "pdf_path":
                            {
                                "type":"string",
                                "description":"this is the path of the pdf where it can be extracted.you must ask the path from the user before calling the function"
                            },
                        "prompt":
                            {
                                "type":"string",
                                "description":"this is an optional prompt .prompt is only given if user asked any extra questions from it or instructions for the pdf summarization."
                            }
                    }
            }
    },
    {"name":"execute_python_code",
    "description":"this is the function to execute python programs.",
    "parameters":{
        "type":"object",
        "properties":{
            "python_code":
                {
                    "type":"string",
                    "description":"the parameter is a python code you have to give input as a python code."
                }
        }
    }    
    },
    {"name":"reminder",
     "description":"this function is used to set an alarm  and load the previous alarms if the parameter of this function is empty it consider as to just only load the reminders .if it has a query it consider as setting the reminder as well as load the reminders as well",
     "parameters":
         {
             "type":"object",
             "properties":{
                 "query":
                     {
                         "type":"string",
                         "description":"This is the query you have to provide with exact date and time followed by the message .the format of query must be YYYY-MM-DD HH:MM(24 hour format) followed by the reminder message.For example:query= set an alarm at 2024-04-01 18:07 to freshup and it is otional "
                     }
             }
         }
     },
    {"name":"take_screen_shot",
     "description":"this function is used to take screenshot of the current window.this function has to be called when user asked."     
     },
    {"name":"generate_images",
     "description":"this function will generate the images the user want you just have to give the proper image prompt to generate the image.",
     "parameters":
         {
             "type":"object",
             "properties":{
                 "prompt":
                     {
                         "type":"string",
                         "description":"this is the prompt you have to give to the function which will generate the user required images .you have to give unbiased prompt here."
                     }
             }
         }
     
    }, 
    { "name":"play_music",
        "description":"plays from  spotify application.",
        "parameters":
            {
                "type":"object",
                "properties":
                    {
                        "song_name":
                            {
                                "type":"string",
                                "description":"song name to play it."
                            }
                    }
            }
    },
    {"name":"send_whatsapp_msg",
        "description":"used to send a message to the whatsapp number",
        "parameters":
            {
                "type":"object",
                "properties":
                    {
                        "receiver":
                            {
                                "type":"string",
                                "description":"the receiver name or his number to send a whatsapp message"
                            },
                        "msg":
                            {
                                "type":"string",
                                "description":"the message to send to the receiver using whatsapp"
                            }
                    }
            }
    },
    { "name":"write_program",
         "description":"write any language program and save it in a file .",
         "parameters":
             {
                 "type":"object",
                 "properties":
                     {
                         "language":
                             {
                                 "type":"string",
                                 "description":"you have to define the language you are writing."
                             },
                            "code":
                                {
                                    "type":"string",
                                    "description":"the program has to be given here to write in a file."
                                },
                                "file_name":
                                    {
                                        "type":"string",
                                        "description":"the file_name of the program where it will be saved.remember if you know the extension of the file you should give it."
                                    }
                     }
             }
     },
    {"name":"read_program_file",
         "description":"reads the program from the file .it may be in any language in your knowledge.",
         "parameters":
             {
                 "type":"object",
                 "properties":
                     {
                         "file_name":
                             {
                                 "type":"string",
                                 "description":"the file_name where the program can be read."
                             }
                     }
             }
     },
    {"name":"play_videos_on_youtube",
         "description":"this function is usedto play youtube videos",
          "parameters":
             {
                 "type":"object",
                 "properties":
                     {
                         "video_name":
                             {
                                 "type":"string",
                                 "description":"this is the video name you have to search it n youtube."
                             }
                     }
             }
     },
    {"name":"summarise_the_youtube_video",
     "description":"this function is used when the user want the summary of the youtube video .remember this function only works for summarising the youtube videos only.",
     "parameters":
         {
             "type":"object",
             "properties":
                 {
                     "video_url":
                         {
                             "type":"string",
                             "description":"this is the youtube video url you have to provide to summarize the video.remember only youube link example:https://www.youtube.com/watch?v=wjZofJX0v4M"
                         }
                 }
         }
    
    },
    
    {"name":"shutdown",
        "description":"shutdown the computer using system call available in operating system."
    },
    {"name":"restart",
        "description":"restart the computer using system call available in operating system."
    },
    {"name":"sleep",
        "description":"put the computer in a sleep mode"
    }
]
