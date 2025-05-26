import os
import requests
from bs4 import BeautifulSoup
import pyttsx3
import speech_recognition as sr

from dotenv import load_dotenv
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
def summarize_content(text,prompt):
    pass
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
