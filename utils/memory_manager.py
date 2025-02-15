from typing import List
import json
import os
from langchain_community.graphs import Neo4jGraph
from langchain.chains.graph_qa.cypher import GraphCypherQAChain 
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.documents import Document
from langchain_ollama import ChatOllama
os.environ["NEO4J_URI"] = "bolt://localhost:7687"
os.environ["NEO4J_USERNAME"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "goutham9"

from utils.config import Config
class MemoryManager:
    def __init__(self):
        self.config=Config()
        self.conversations=[]
        self.graph=Neo4jGraph()
        self.llm=ChatOllama(temperature=0,model="qwen2.5:0.5b")
        self.llm_transformer=LLMGraphTransformer(llm=self.llm)
    def add_conversation(self, user_message: str, response: str,user_name:str):
        """Add conversation to memory"""
        # Add user and assistant messages to the memory
        conversation={
            "user":user_name,
            "user_message":user_message,
            "assistant":"rolex",
            "assistant_response":response
        }
        documents=[Document(page_content=user_message)]
        graph_documents=self.llm_transformer.convert_to_graph_documents(documents)
        print(f"nodes:{graph_documents[0].nodes}\nrelationships:{graph_documents[0].relationships}")
        self.graph.add_graph_documents(graph_documents)
        self.conversations.append(conversation)
        with open("history.json","a") as f: 
            json.dump(conversation,f)
        
    def get_recent_conversations(self, user_message:str,user_id:str,limit: int = 10) -> List[dict]:
        """Get recent conversations from memory"""
        self.graph.refresh_schema()
        print("graphdb schema:",self.graph.structured_schema)
        chain=GraphCypherQAChain.from_llm(llm=self.llm,graph=self.graph,verbose=True)
        response=chain.invoke({"query":f"Find the information about {user_message}"})
        print(response)
        return str(response)