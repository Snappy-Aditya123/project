from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
import streamlit as st
import DBMS  # Your database module

class ChatbotAgent:
    def __init__(self, model="llama3", Keepalive=False):
        self.llm = ChatOllama(model=model, temperature=0.7, keep_alive=Keepalive,num_predict=300,num_thread=6)
    
        self.db = DBMS.ChatDatabase()

    def chat(self, message):
        # Append new user message to memory
        # Send full conversation history to the chatbot
        response = self.llm.stream(message)
        # Save conversation in the database
        full_response = ""
        for chunk in response:
            full_response += chunk.content
            yield chunk.content
        self.db.insert_chat(message[-1].content,full_response )
        
