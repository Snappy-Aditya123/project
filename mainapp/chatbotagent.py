from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
import streamlit as st
import DBMS  # Your database module
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

class ChatbotAgent:
    def __init__(self, model="llama3", keep_alive=False, history_limit=10):
        self.llm = ChatOllama(model=model, temperature=0.7, keep_alive=keep_alive, num_predict=300, num_thread=6)
        self.vector_db = Chroma(persist_directory="chroma_db", embedding_function=OllamaEmbeddings(model="nomic-embed-text"))
        self.db = DBMS.ChatDatabase()
        self.history_limit = history_limit

    def summarize_conversation(self, messages):
        summary_prompt = f"Summarize the following conversation concisely reatning makor infos like names,ages,numbers and important parts only:\n{messages}"
        summary = self.llm.invoke([HumanMessage(summary_prompt)]).content  # Using LLM for summarization
        return summary

    def trim_chat_history(self, message_history):
        if len(message_history) > self.history_limit:
            # Summarize older messages
            summary = self.summarize_conversation(message_history[:-self.history_limit])
            summarized_message = SystemMessage(f"Summary of previous conversation: {summary}")
            return [summarized_message] + message_history[-self.history_limit:]
        return message_history

    def chat(self, message_history):
        if not message_history:
            return
        
        # Trim chat history to manage memory efficiently
        message_history = self.trim_chat_history(message_history)
        
        # Extract latest user message
        last_message = message_history[-1]
        user_prompt = last_message.content
        
        # Retrieve relevant documents
        retriever = self.vector_db.as_retriever()
        context_docs = retriever.get_relevant_documents(user_prompt)
        formatted_context = "\n\n".join(doc.page_content for doc in context_docs) if context_docs else ""
        
        # Create system message (not stored in message history)
        system_message = SystemMessage(f"""
        Context from vector DB (for reference only, do not let it bias responses):
        {formatted_context}
        
        You are not allowed to talk about anything apart from job and professional-related topics.
        """)
        
        # Prepare input messages (system message + chat history)
        input_messages = [system_message] + message_history
        
        # Generate response using LLM
        response = self.llm.stream(input_messages)
        # Save conversation in the database
        full_response = ""
        for chunk in response:
            full_response += chunk.content
            yield chunk.content
        # Collect response and save conversation
        self.db.insert_chat(user_prompt, full_response)
        
