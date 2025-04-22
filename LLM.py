from fastapi import FastAPI, Request
from pydantic import BaseModel
from openai import OpenAI
import json

# 读取API Key
with open("keys.json", "r") as f:
    api_key = json.load(f)["deepseek"]

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
app = FastAPI()

class ChatRequest(BaseModel):
    messages: list  # [{"role": "user", "content": "..."}]

@app.post("/chat")
def chat(req: ChatRequest):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": "You are a helpful assistant."}] + req.messages,
        stream=False
    )
    return {"reply": response.choices[0].message.content}