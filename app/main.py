from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

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
        "status": "healthy"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    global agent

    # Lazy import to avoid heavy startup during deployment
    if agent is None:
        from app.agent import SHLAgent
        agent = SHLAgent()

    messages = [
        {
            "role": m.role,
            "content": m.content
        }
        for m in request.messages
    ]

    return agent.chat(messages)