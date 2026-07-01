from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from app.agent import SHLAgent

app = FastAPI(
    title="SHL Assessment Recommendation API",
    description="Conversational AI assistant for recommending and comparing SHL assessments using RAG and Gemini.",
    version="1.0"
)

agent = SHLAgent()


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


# ----------------------------
# Health Check (Required by SHL)
# ----------------------------
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "SHL Assessment Recommendation API"
    }


# ----------------------------
# Chat Endpoint
# ----------------------------
@app.post("/chat")
def chat(request: ChatRequest):

    messages = [
        {
            "role": m.role,
            "content": m.content
        }
        for m in request.messages
    ]

    response = agent.chat(messages)

    return response