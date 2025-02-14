from typing import List
from mem0 import Memory
from utils.config import Config
class MemoryManager:
    def __init__(self):
        self.config=Config()
        self.memory = Memory.from_config({
            "llm":{
                "provider":"gemini",
                "config":{
                    "model":"gemini-1.5-flash-latest",
                    "temperature":0.2,
                    "max_tokens":1500,
                    "api_key":self.config.GEMINI_API_KEY
                }
            },
            "embedder":{
                "provider":"gemini",
                "config":{
                    "model":"models/text-embedding-004",
                    "api_key":self.config.GEMINI_API_KEY,
                    "embedding_dims":768,
                }
            },
            "vector_store": {
        "provider": "pgvector",
        "config": {
            
            "user": "postgres",
            "password": "goutham9",
            "host": "127.0.0.1",
            "port": "5432",
            "embedding_model_dims":768,
        }
    }
        })
        
        
    def add_conversation(self, user_message: str, response: str,user_name:str):
        """Add conversation to memory"""
        # Add user and assistant messages to the memory
        
        self.memory.add([{
                "role": "user","content":user_message},{
                "role":"assistant","content": response
            }],user_id=user_name,agent_id="rolex")
        
    def get_recent_conversations(self, user_message:str,limit: int = 10) -> List[dict]:
        """Get recent conversations from memory"""
        relevant_memories=self.memory.search(query=user_message,user_id="default_user",limit=3)
        memory_str="\n".join(f"-{entry['memory']}" for entry in relevant_memories)
        return memory_str
