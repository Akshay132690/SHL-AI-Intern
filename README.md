# SHL Assessment Recommendation System

An AI-powered conversational assistant that recommends the most relevant SHL assessments based on hiring requirements. The system uses Retrieval-Augmented Generation (RAG) by combining semantic search with Google's Gemini model to provide intelligent recommendations.

## Features

- Conversational assessment recommendation
- Multi-turn conversation support
- SHL assessment comparison
- Recommendation refinement
- Semantic search using FAISS
- AI-generated recommendation explanations
- REST API built with FastAPI
- Health check endpoint for deployment monitoring

---

## Tech Stack

- Python
- FastAPI
- Google Gemini 2.5 Flash
- Sentence Transformers
- FAISS
- NumPy
- Render
- GitHub

---

## Project Structure

```
SHL-AI-Intern/
│
├── app/
│   ├── agent.py
│   ├── comparison.py
│   ├── llm.py
│   ├── main.py
│   ├── memory.py
│   ├── recommender.py
│   ├── retriever.py
│   ├── state.py
│   ├── validator.py
│   └── build_index.py
│
├── vector_db/
│   ├── shl.index
│   └── documents.pkl
│
├── data/
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## System Architecture

```
User
   │
   ▼
FastAPI API
   │
   ▼
Gemini (Intent Analysis)
   │
   ▼
Conversation Memory
   │
   ▼
Recommendation Engine
      │
      ▼
FAISS Vector Search
      │
      ▼
Gemini Explanation
      │
      ▼
Recommended SHL Assessments
```

---

## API Endpoints

### Health Check

```
GET /health
```

Response

```json
{
  "status": "healthy"
}
```

---

### Chat Endpoint

```
POST /chat
```

Example Request

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Need assessment for Java Backend Developer"
    }
  ]
}
```

---

## Running Locally

### Clone the repository

```bash
git clone <repository-url>
cd SHL-AI-Intern
```

### Create virtual environment

```bash
python -m venv venv
```

Activate the environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

Create a `.env` file.

```
GEMINI_API_KEY=YOUR_API_KEY
```

### Run the application

```bash
uvicorn app.main:app --reload
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## Recommendation Workflow

1. User submits hiring requirements.
2. Gemini extracts role, skills, seniority, and intent.
3. Conversation memory stores context.
4. FAISS retrieves relevant SHL assessments.
5. Recommendation engine ranks results using business rules.
6. Gemini generates a natural language explanation.
7. API returns the recommended assessments.

---

## Deployment

The application is deployed on Render.

API Base URL

```
https://shl-ai-assistant-cbom.onrender.com
```

Swagger Documentation

```
https://shl-ai-assistant-cbom.onrender.com/docs
```

Health Check

```
https://shl-ai-assistant-cbom.onrender.com/health
```

---

## AI Tools Used

- Google Gemini API for conversation understanding, recommendation explanation, and assessment comparison.
- ChatGPT for architecture discussions, debugging, deployment troubleshooting, and prompt refinement.

---

## Future Improvements

- Assessment caching to reduce LLM calls
- Support for multiple LLM providers
- User authentication
- Conversation history persistence
- Enhanced recommendation ranking
- Automated evaluation metrics

---

## License

This project was developed as part of the SHL AI Internship Assignment.
