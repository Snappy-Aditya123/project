from typing import Dict, any
import json
from openai import OpenAI

class BaseAgent:
    def __init__(self,name:str,instructions:str):
        self.name = name
        self.insctructions =instructions
        self.ollama_client = OpenAI(
            base_url = "http://localhost:11434/v1",
            api_key = "ollama",
        )
    async def run(self,message: list) -> Dict[str, any]:
        raise NotImplementedError("subclasses must implement run method")
    
    def _query_ollama(self, prompt:str) -> str:
        try:
            response = self.ollama_client.chat.completions.create(
                model = self.name,
                messages = [{"role": "system","content":self.insctructions},
                            {"role": "user", "content": prompt}
                            ],
                temperature= 0.5,
                max_tokens=300,
            )
            return response.choices[0].message.content
        except Exception as e:
            return str(e)

    def _pare_json_safely(self, text:str) -> Dict[str, any]:
        try:
            start = text.find("{")
            end = text.rfind("}") 
            if start != -1 and end != -1:
                json_str = text[start:end+1]
                return json.loads(json_str)
            return {"error": "No JSON found"}
        except json.JSONDecodeError as e:
            return {"error": str(e)}
    
    