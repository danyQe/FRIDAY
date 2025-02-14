from typing import Optional,Union
import os
import pyautogui
import time
import subprocess
import PyPDF2
from deep_translator import GoogleTranslator
import datetime
from youtube_transcript_api import YouTubeTranscriptApi
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import pywhatkit
from google import genai
from utils.helpers import fix_content,summarize_content,speak,get_voice_input
from utils.config import Config
from pydantic import BaseModel

#the user functions called by gemini
def web_scrape(url: str) -> dict[str, str]:
    """Scrapes content from a webpage using Microsoft Edge.
    
    Args:
        url: The URL of the webpage to scrape.
        
    Returns:
        A dictionary
    """
    try:

         driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
     
         driver.get(url)
         html_content=driver.page_source
         driver.quit()

         soup=BeautifulSoup(html_content,'html.parser')
         text=soup.get_text(separator='\n')
         links=[link.get('href') for link in soup.find_all('a')  if link.get("href")]
         
         return {
             "text":text,
             "links":links,
             "status":"success"
         }
    except Exception as e:
            return{
                "status":"error",
                "error":str(e)
            }
def open_application(app_name: str) -> dict[str, str]:
    """Opens a Windows application using the Start menu.
    
    Args:
        app_name: Name of the application to open.
        
    Returns:
        A dictionary containing the operation status.
    """
    try:
         pyautogui.press('win')
         time.sleep(1) 
         pyautogui.write(app_name, interval=0.1) 
         time.sleep(1) 
         pyautogui.press('enter')
         return {"status": "success", "message": f"Opened {app_name} successfully"}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def get_date_and_time()->dict[str,Union[str,int,float]]:
    """
    use this function to retreive  the current date and time using datetime python library.
    
    Returns:
        A dictionary containing the operation status and current date and time.
    
    """
    try: 
        now = datetime.datetime.now()
        date_string = now.strftime("%Y-%m-%d")
        time_string = now.strftime("%I:%M:%S %p")
        return {
            "status":"success",
            "time":time_string,
            "date":date_string
        }
    except Exception as e:
        return {
            "status":"error",
            "error":str(e)
        }

def translate_text(text: str, target_language: str) -> dict[str, str]:
    """Translates text to the specified language.
    
    Args:
        text: Text to translate.
        target_language: Target language code (default: "en" for English).
        
    Returns:
        A dictionary containing the translated text and detected language.
    """
    try:
        translator = GoogleTranslator(source='auto', target=target_language)
        translation = translator.translate(text)
        return {
            "translated_text": translation,
            "target_language": target_language,
            "status": "success"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

def summarize_pdf(pdf_path: str, prompt: Optional[str] = None) -> dict[str, str]:
    """Extracts and summarizes text from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file.
        prompt: Optional specific instructions for summarization.
        
    Returns:
        A dictionary containing the summarized text.
    """
    try:
        text = ""
        if not os.path.exists('documents'):
            # Create the directory if it doesn't exist
            os.makedirs('documents')
        with open(os.path.join('documents', pdf_path), 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                text += page.extract_text()
            return {
            "text": text,
            "prompt": prompt,
            "status": "success"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
def execute_python_code(python_code: str) -> dict[str, str]:
    """
    Executes the given Python code in a temporary file and returns the output.

    Args:
        python_code: The Python code to execute.

    Returns:
        A dictionary containing execution results and the status.
    """
    try:
        # Save the code to a temporary file
        with open("temp_code.py", "w") as file:
            file.write(python_code)

        # Define the command to execute the temporary Python file
        command = ["python", "temp_code.py"]

        # Execute the command and capture output
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        # Return results in a dictionary
        return {
            "status": "success" if process.returncode == 0 else "failed",
            "results": stdout.strip() if stdout else stderr.strip()
        }

    except Exception as e:
        return {"status": "error", "results": str(e)}

def play_music(song_name: str) -> dict[str, str,str]:
    """Plays a song on Spotify.
    
    Args:
        song_name: Name of the song to play.
        
    Returns:
        A dictionary containing the playback status.
    """
    # Press Windows key to open Start menu
    try:
        pyautogui.press('win')
        time.sleep(2)
    
        # Type "Spotify" to search for Spotify and press Enter
        pyautogui.write('Spotify')
        time.sleep(2)
        pyautogui.press('enter')
        # Wait for Spotify to load
        time.sleep(10)
    
        # Focus on the Spotify window
        spotify_window = pyautogui.getWindowsWithTitle("Spotify")[0]
        spotify_window.maximize()
    
        # Focus on the search bar
        pyautogui.hotkey('ctrl', 'k')
        time.sleep(3)
    
        # Type the song name in the search bar and press Enter
        pyautogui.write(song_name, interval=0.2)
        time.sleep(5)
        pyautogui.press('enter')
        time.sleep(1)
        # Select the first search result (assuming it's the desired song)
        # Check if the song started playing
        time.sleep(5)  # Wait for the song to start playing
        return {
            "song": song_name,
            "status": "success",
            "message": f"Playing {song_name}"
        }
    except Exception as e:
          return {
            "song":song_name,
            "status": "error",
            "error": str(e)
        }

def send_whatsapp_msg(receiver: str, msg: str) -> dict[str, str]:
    """
    Automates sending a WhatsApp message using pyautogui.

    This function simulates keyboard interactions to open WhatsApp, search for the specified receiver,
    and send the provided message.

    Args:
        receiver (str):provide The contact name to search it in whatsapp and rest will be done by the pyautogui itself.rememember don't ask the number form the user it compromises the privacy.
        msg (str): The message content.

    Returns:
        dict[str, str]: A dictionary with the status and a message detailing the outcome.
    """
    try:
        pyautogui.hotkey('win')
        time.sleep(3)
        pyautogui.write('whatsapp')
        time.sleep(7)
        pyautogui.press('enter')
        time.sleep(10)
        pyautogui.write(receiver, interval=0.2)
        pyautogui.hotkey('enter')
        time.sleep(8)
        pyautogui.press('tab')
        time.sleep(7)
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.write(msg, interval=0.3)
        time.sleep(7)
        pyautogui.hotkey('enter')
        time.sleep(10)
        pyautogui.hotkey('alt', 'f4')
        
        return {"status": "success", "message": "Message sent successfully."}
    
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "error", "message": str(e)}

def write_program(language: str, code: str, file_name: str) -> dict[str, str]:
    """
    Writes a computer program to a file.

    Args:
        language (str): The programming language of the code.
        code (str): The code to be written to the file.
        file_name (str): The desired file name without extension.

    Returns:
        dict[str, str]: A dictionary containing the status and file path or an error message.
    """
    # Language to file extension mapping
    file_extensions = {
        "python": ".py",
        "java": ".java",
        "c++": ".cpp",
        "javascript": ".js",
        "c": ".c",
        "sql": ".sql"
    }
    
    file_extension = file_extensions.get(language.lower())
    
    if file_extension is None:
        return {"status": "error", "message": f"Unsupported language: {language}"}

    # Sanitize and format the code
    # Assuming fix_content is a function that formats/cleans the code
    try:
        code = fix_content(code)
    except Exception as e:
        return {"status": "error", "message": f"Error formatting code: {e}"}

    # Ensure correct file extension
    if not file_name.endswith(file_extension):
        file_name += file_extension

    # Define the directory path
    directory = "programs"
    os.makedirs(directory, exist_ok=True)  # Ensure directory exists

    file_path = os.path.join(directory, file_name)

    # Write the code to the file
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
        return {"status": "success", "file_path": file_path}
    except Exception as e:
        return {"status": "error", "message": f"Error writing to file: {e}"}
def read_program_file(file_name: str) -> dict[str, Union[str, None]]:
    """
    Reads a program file from the 'programs' directory and returns its contents.

    Args:
        file_name (str): The name of the file to read.

    Returns:
        dict[str, Union[str, None]]: A dictionary with status and either the code or an error message.
    """
    file_path = os.path.join("programs", file_name)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        return {"status": "success", "code": code}
    
    except FileNotFoundError:
        return {"status": "error", "message": f"File '{file_name}' not found"}
    
    except Exception as e:
        return {"status": "error", "message": f"Error reading file '{file_name}': {e}"}
def play_videos_on_youtube(video_name: str) -> dict[str, str]:
    """
    Searches and plays a video on YouTube using pywhatkit.

    Args:
        video_name (str): The name of the video to search and play.

    Returns:
        dict[str, str]: A dictionary containing the status and a message.
    """
    try:
        pywhatkit.playonyt(video_name)
        return {"status": "success", "message": "Successfully playing the YouTube video."}
    except Exception as e:
        return {"status": "error", "message": f"Error occurred while playing YouTube video: {e}"}

def summarise_the_youtube_video(video_url: str) -> dict[str, str]:
    """
    Extracts and summarizes the transcript of a YouTube video.

    Args:
        video_url (str): The URL of the YouTube video.

    Returns:
        dict[str, str]: A dictionary containing the status and either the summary or an error message.
    """
    try:
        # Extract video ID from URL
        if "watch?v=" in video_url:
            video_id = video_url.split("watch?v=")[1].split("&")[0]  # Handles additional query params
        elif "youtu.be/" in video_url:
            video_id = video_url.split("youtu.be/")[1].split("?")[0]  # Handles shortened URLs
        else:
            return {"status": "error", "message": "Invalid YouTube URL format."}

        # Fetch transcript
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        # Construct full transcript
        transcript = "This is the YouTube video content. Summarize accordingly:\n"
        transcript += " ".join([i["text"] for i in transcript_text])

        # Summarize content
        summary = summarize_content(transcript)

        return {"status": "success", "summary": summary}

    except Exception as e:
        return {"status": "error", "message": f"Error occurred while transcribing: {e}"}



def call_on_whatsapp(receiver: str) -> dict[str, str]:
    """
    Initiates a voice call on WhatsApp with the given receiver name.

    Args:
        receiver (str): Name of the WhatsApp contact to call.

    Returns:
        Dict[str, str]: A dictionary containing status and message.
    """
    try:
        pyautogui.hotkey('win')
        time.sleep(3)
        pyautogui.write('whatsapp')
        time.sleep(7)
        pyautogui.press('enter')
        # subprocess.Popen(["C:\\Users\\YourUsername\\AppData\\Local\\WhatsApp\\WhatsApp.exe"])  # Update path if needed
        time.sleep(5)

        pyautogui.write(receiver, interval=0.1)
        pyautogui.press("enter")
        time.sleep(2)

        # Navigating to the call button
        for _ in range(11):
            pyautogui.press("tab")

        pyautogui.press("enter")
        time.sleep(2)

        return {"status": "success", "message": f"Voice call initiated to {receiver} on WhatsApp."}

    except Exception as e:
        with open("error.txt", "a", encoding="utf-8") as f:
            f.write(f"Error calling {receiver}: {e}\n")

        speak("Sorry, I encountered an error while making the call.")
        return {"status": "error", "message": f"Error occurred: {e}"}

def videocall_on_whatsapp(receiver: str) -> dict[str, str]:
    """
    Initiates a video call on WhatsApp with the given receiver name.

    Args:
        receiver (str): Name of the WhatsApp contact to call.

    Returns:
        Dict[str, str]: A dictionary containing status and message.
    """
    try:
        pyautogui.hotkey('win')
        time.sleep(3)
        pyautogui.write('whatsapp')
        time.sleep(7)
        pyautogui.press('enter')
        # subprocess.Popen(["C:\\Users\\YourUsername\\AppData\\Local\\WhatsApp\\WhatsApp.exe"])  # Update path if needed
        time.sleep(5)

        pyautogui.write(receiver, interval=0.1)
        pyautogui.press("enter")
        time.sleep(2)

        # Navigating to the video call button
        for _ in range(10):
            pyautogui.press("tab")

        pyautogui.press("enter")
        time.sleep(2)

        return {"status": "success", "message": f"Video call initiated to {receiver} on WhatsApp."}

    except Exception as e:
        with open("error.txt", "a", encoding="utf-8") as f:
            f.write(f"Error video calling {receiver}: {e}\n")

        speak("Sorry, I encountered an error while making the video call.")
        return {"status": "error", "message": f"Error occurred: {e}"}

class Description(BaseModel):
    current_window_description:str="clearly describes what the windows is actually showing "
class Output(BaseModel):
    code:str
    current_window_description:str
isdone=False
def control_gui(prompt:str)->dict[str,str]:
    """
    Use this function to control gui using pyautoigui .write a detailed prompt to acheive the desired task for example move mouse to certain points(x,y) or write something in the input box or click function etc.
    this tasks are achived using pyautogui in python and a AI agent who takes input prompt from you and control it accordingly.
    
    Args: 
         prompt:provide a detailed structured prompt which can be used to control the pc .don't provide unrelated prompts 
         example:
                1)type weather
                2)open whatsapp
                3)press enter
                4)close the current window.
    Returns:
        A dictionary containing the status ,current page details.
    """
    global isdone
    try:
        config=Config()
        while not isdone:
            image=pyautogui.screenshot()
            client=genai.Client(api_key=config.GOOGLE_API_KEY)
            analyser_response=client.models.generate_content(
                model="gemini-1.5-flash",
                contents=[f"You are a system screenshot analyser where you analyse the screenshots of the pc and clearly describes it so that the execute agent will execute based on your instructions .now Analyse this screenshot and clearly describe what you see The task is : {prompt} .so if you can describe the task properly the execute agent will do the execution,here is the current window screenshot:",image],
                config={
                    'response_mime_type':'text/x.enum',
                    'response_schema':str(Description),
                }
            )
            print("analyser_response:",analyser_response.text)
            
            
            
    except Exception as e:
        return  {"status": "error", "message": f"Error occurred while controlling gui: {e}"}
#system commands called by gemini
def shutdown() -> dict[str, str]:
    """
    Shuts down the PC based on user confirmation.

    Returns:
        dict[str, str]: A dictionary with status and message.
    """
    try:
        speak("Do you really want to shut down this PC?")
        shutdown_response = get_voice_input().lower()
        
        if shutdown_response == 'yes':
            os.system("shutdown /s /t 1")
            return {"status": "success", "message": "Shutting down the PC."}
        else:
            speak("Okay, shutdown cancelled.")
            return {"status": "cancelled", "message": "User cancelled shutdown."}
    
    except Exception as e:
        return {"status": "error", "message": f"Error occurred while shutting down: {e}"}

def restart() -> dict[str, str]:
    """
    Restarts the PC based on user confirmation.

    Returns:
        dict[str, str]: A dictionary with status and message.
    """
    try:
        speak("The PC is restarting now.")
        time.sleep(2)
        speak("Do you really want to restart your PC?")
        
        restart_response = get_voice_input().lower()
        if restart_response == 'yes':
            subprocess.call(["shutdown", "-r", "-t", "0"])
            return {"status": "success", "message": "Restarting the PC."}
        else:
            speak("Restart cancelled.")
            return {"status": "cancelled", "message": "User cancelled restart."}
    
    except Exception as e:
        return {"status": "error", "message": f"Error occurred while restarting: {e}"}

def sleep() -> dict[str, str]:
    """
    Puts the PC into sleep mode.

    Returns:
        dict[str, str]: A dictionary with status and message.
    """
    try:
        speak("The PC is going to sleep now.")
        time.sleep(3)
        os.system("Rundll32.exe Powrprof.dll,SetSuspendState Sleep")
        return {"status": "success", "message": "PC is now in sleep mode."}
    
    except Exception as e:
        return {"status": "error", "message": f"Error occurred while putting PC to sleep: {e}"}    

functions=[
        web_scrape,
        open_application,
        get_date_and_time,
        translate_text,
        summarize_pdf,
        play_music,
        send_whatsapp_msg,
        write_program,
        read_program_file,
        play_videos_on_youtube,
        summarise_the_youtube_video,
        call_on_whatsapp,
        videocall_on_whatsapp,
        shutdown,
        sleep,
        restart
        # recognise_face_emotions_and_age,
]

