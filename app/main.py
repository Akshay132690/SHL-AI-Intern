from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from app.agent import SHLAgent

app = FastAPI(
    title="SHL Assessment Recommendation API",
    description="Conversational AI assistant for recommending and comparing SHL assessments using RAG and Gemini.",
    version="1.0"
)

# Lazy initialization
agent = None


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


@app.get("/")
def home():
    return {
        "message": "SHL Assessment Recommendation API is running."
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "SHL Assessment Recommendation API"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    global agent

    # Create the agent only when the first request arrives
    if agent is None:
        print("Initializing SHL Agent...")
        agent = SHLAgent()

    messages = [
        {
            "role": m.role,
            "content": m.content
        }
        for m in request.messages
    ]

    return agent.chat(messages)