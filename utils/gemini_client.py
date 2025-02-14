from google import genai
from google.genai import types
import time
from typing import Optional
from utils.rate_limiter import RateLimiter
from functions import functions
from utils.prompt import prompts
from utils.memory_manager import MemoryManager

class GeminiClient:
    def __init__(self, api_key: str, rate_limiter: RateLimiter):
        self.client = genai.Client(api_key=api_key)
        self.rate_limiter = rate_limiter
        self.config=types.GenerateContentConfig(tools=functions,system_instruction=prompts["friday"])
        self.memory=MemoryManager()
        self.chat = self.client.chats.create(model="gemini-1.5-flash",config=self.config)
        
    def send_message(self, message: str, user_name:str,history: Optional[list] = None) -> str:
        estimated_tokens = len(message.split()) * 2  # Rough estimation
        
        if not self.rate_limiter.can_make_request(estimated_tokens):
            raise Exception("Rate limit exceeded. Please try again later.")
            
        try:
            print("chat:",self.chat._curated_history)
            memories=self.memory.get_recent_conversations(user_message=message,user_id=user_name)
            print("previous_memories:",memories)
            response = self.chat.send_message(f"{message}\nrelevant memories :{str(memories)}")
            # print("response:",response)
            print("friday:",response.text)
            for message in self.chat._curated_history:
                print(f'role - ', message.role, end=": ")
                print(message.parts[0].text)
            self.memory.add_conversation(message,response.text,user_name)
            if response.candidates[0].content.parts[0].function_call:
                function_call=response.candidates[0].content.parts[0].function_call
                print("function_called:",function_call.name)
                print("function_parameters:",function_call.args)
            return response.text
        except Exception as e:
            raise Exception(f"Error communicating with Gemini: {str(e)}")
