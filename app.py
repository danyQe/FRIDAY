import requests
import json
import os
import webbrowser
from threading import Timer,Thread,Event,Lock
from dotenv import load_dotenv
from utils.prompt import prompts
from flask import Flask, render_template, request, jsonify,send_from_directory
import_lock=Lock()
def import_functions():
    global functions
    with import_lock:
         print("importing functions and neccessary libraries.........\n")
         import functions
         print("the functions successfully imported\n")
import_thread=Thread(target=import_functions)
import_thread.start()
print("starting the voice assistant......\n")
import_thread.join()
app = Flask(__name__, static_folder='static', template_folder='templates')

class Backend:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.system_message_flag = ''
        self.stop_event=Event()
        self.messages=[]
        self.messages1=[]
        self.backup_messages=[]
        self.headers = {
    'Content-Type': 'application/json'
      }
    def count_tokens(self,message):
        try:
            data1={
                    "contents":[message]
                }
            count_tokens_response=requests.post("https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:countTokens?key="+self.api_key,json=data1,headers=self.headers)
            count_token=count_tokens_response.json()
            print(count_token)
            total_tokens=count_token.get('totalTokens')
            print(total_tokens)
            return total_tokens
        except Exception as e:
             print(f"unable to count tokens reason :{e}")
    def write_list_to_file(self, lst, filename):
        with open(filename, 'a', encoding='utf-8') as file:
            for item in lst:
                file.write(str(item) + '\n')

    def parse_function_response(self,function_name,function_args):
        print("Gemini: Called function " + function_name )

        try:
            arguments = function_args
            print("arguments:",arguments)
            if hasattr(functions, function_name):
                function_response = getattr(functions, function_name)(**arguments)
            else:
                function_response = "ERROR: Called unknown function"
        except TypeError as e:
            function_response = f"ERROR: Invalid arguments:{e}"
        fmessage = {
                "role": "function",
                "parts": [
                    {
                        "functionResponse": {
                            "name": function_name,
                            "response": {
                                "name": function_name,
                                "content": function_response
                            }
                        }
                    }
                ]
            }
            
            # Save the function response to the JSON file and append to messages
        with open("messages.json", "a") as f:
                f.write(json.dumps(fmessage, indent=4))
        self.messages.append(fmessage)
    

        return self.process_message()

    
    def gemini(self):
        count_tokens=0
        data = {
            "contents": [self.messages],
            "tools": [{
                "functionDeclarations": functions.function_definitions
            }

            ],
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_ONLY_HIGH"
                },
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_ONLY_HIGH"

                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_ONLY_HIGH",
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_LOW_AND_ABOVE",
                },
            ],
           "generationConfig": {
            "temperature": 0.3
        }
            
        }
        # count_tokens_response=requests.post("https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:countTokens?key="+self.api_key,json=data1,headers=headers)
        
        if(self.count_tokens(self.messages)<30720):
            response = requests.post("https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" +self.api_key, json=data)
            if response.status_code != 200:
                print(f"errorcode:200->{response.text}")
                if response.status_code==500:
                    self.messages=[]
                    return f"an iternal server has occured on google please try reloading the page."
                if response.status_code==400:
                    return f"an  internal server error please make sure the requsest is between user and model"
                return f"unable to send a request to the gemini server please reload the page to try again"
        else:
               messag=self.summarize_content(self.messages)
               return f"reduced content after the summarization:{messag}"
        response = response.json()
        if "candidates" not in response:
            return "an internal error has occured .something with the prompt handling.contact developer to solve this error."
        if "content" not in response["candidates"][0]:
            message={
                "role":"model",
                "parts":"i am sorry i am unable to generate the response"
            }
            self.messages.append(message)
            return f"unable to  generated  the response.try again. "

        message = response['candidates'][0]['content']['parts']
        message1={
                "role": "model",
                "parts": message
            }
        with open("messages.json", "a") as f:
                f.write(json.dumps(message1, indent=4))
        self.messages.append(message1)
        return message
    def process_message(self):
        text_content = None
        function_name = None
        function_args = None
        message=self.gemini()
        # Parse through each part in the message to handle text and function call
        for part in message:
            if "text" in part:
                text_content = part["text"]
            if "functionCall" in part:
                function_name = part["functionCall"].get("name")
                function_args = part["functionCall"].get("args")
    
        # Process function call if present
        if function_name:
            # Execute function call
            return self.parse_function_response(function_name, function_args)
        return text_content  # Return only text if present


    def call_gemini(self, system_message=None):
        if system_message:
            message = {"role": "user", "parts": [{"text": system_message}]}
            with open("messages.json", "a") as f:
                f.write(json.dumps(message, indent=4))
            self.messages=[]
            self.messages.append(message)
        response = self.process_message()
        if response:
            print("bot:", response)
            self.system_message_flag = response
        else:
            self.system_message_flag = ''

    def send_system_message(self):
        if self.system_message_flag:
            message = self.system_message_flag
            self.system_message_flag = ''
            print("Sending it to the client")
            return jsonify({'message': message,'messages':self.messages})
        else:
            return jsonify({'message': '','messages':self.messages})

    def send_message(self):
        print("Send message endpoint is called")
        data = request.json
        message = data.get('message', '')
        if not message:
            print("No message is provided by the server")
        message = {
                "role": "user",
                "parts": [{"text": message}]
            }
        with open("messages.json", "a") as f:
                f.write(json.dumps(message, indent=4))
        self.messages.append(message)
        bot_response = self.process_message()
        print(f"sending to the server:{bot_response}")
        return jsonify({'message': bot_response,'messages':self.messages})
    def send_pdf(self,message):
        with open("messages.json", "a") as f:
                f.write(json.dumps(message, indent=4))
        self.messages.append(message)
        response=self.process_message()
        print(f"sending to the server:{response}")
        return jsonify({'message':response,'messages':self.messages})
    def restart_server(self):
        print("restarting")
        self.messages=self.backup_messages
        bot_response = self.gemini()
        # self.speak_async(bot_response)
        return jsonify({'message': bot_response,'messages':self.messages})

def check_env_file():
    try:
        with open('.env', 'r') as f:
            for line in f:
                if 'GOOGLE_API_KEY' in line:
                    google_key_found = True
            if google_key_found:
                return True
        return False
    except FileNotFoundError:
        return False
@app.route('/check_keys', methods=['GET'])
def check_keys():
    keys_present = check_env_file()
    return jsonify({'keys_present': keys_present})
@app.route('/save_keys', methods=['POST'])
def save_keys():
    data=request.get_json()
    google_api_key = data.get('google_api_key','')

    with open('.env', 'w') as f:
        f.write(f"""GOOGLE_API_KEY="{google_api_key}"\n""")
        f.write(f"""TF_ENABLE_ONEDNN_OPTS=0\n""")

    return jsonify({'success': True})



backend = Backend()

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/no_camera_input')
def no_camera_input():
    system_message =prompts[1]['start_without_camera']
    backend.call_gemini(system_message=system_message)
    return render_template("input.html")
@app.route('/input')
def input():
    system_message =prompts[0]['start_with_camera']
    backend.call_gemini(system_message=system_message)
    return render_template('input.html')
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return  jsonify({"message":"no file part"})
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and file.filename.endswith('.pdf'):
        # Save the file to a desired location
        if not os.path.exists("documents"):
             os.makedirs("documents")
        file.save(os.path.join('documents', file.filename))
        print(file.filename)
        message = {
                "role": "user",
                "parts": [{"text": f"summarize the {file.filename} file"}]
            }
        return  backend.send_pdf(message) 
    else:
        return 'File upload failed: Only PDF files are allowed'
@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

@app.route('/resources')
def resources():
    return render_template('references.html')
@app.route('/images')
def show_images():
    output_dir='output'
    if not os.listdir(output_dir):
        return jsonify({'error': 'Output directory is empty'})
    return send_from_directory()
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/send_system_message', methods=['POST'])
def send_system_message():
    return backend.send_system_message()

@app.route('/send_message', methods=['POST'])
def send_message():
    return backend.send_message()

@app.route('/restart_backend', methods=['POST'])
def restart_backend():
    return backend.restart_server()
def open_browser():
    webbrowser.open('http://localhost:5000')

if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(debug=True,host= "0.0.0.0",port="5000")
