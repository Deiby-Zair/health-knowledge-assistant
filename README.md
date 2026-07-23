# 🩺 Health Knowledge Assistant

An AI-powered Retrieval-Augmented Generation (RAG) assistant that provides reliable information about the Colombian healthcare system using semantic search and Large Language Models.

Built with a decoupled architecture featuring a **FastAPI backend**, **Next.js frontend**, and **Qdrant vector database**.

## Features

* 🔎 Retrieval-Augmented Generation (RAG)
* 🧠 Semantic search with vector embeddings
* 📖 Source-aware responses with citations
* 🔄 Provider-agnostic LLM integration (OpenAI & Gemini)
* ⚡ FastAPI REST API
* 💬 Modern chat interface with Next.js
* 🏗️ Modular and scalable architecture

## Tech Stack

| Backend       | AI / RAG              | Frontend     |
| ------------- | --------------------- | ------------ |
| Python        | OpenAI                | Next.js      |
| FastAPI       | Google Gemini         | React        |
| Uvicorn       | Qdrant                | TypeScript   |
| Pydantic      | Sentence Transformers | Tailwind CSS |
| python-dotenv | Prompt Engineering    | Lucide React |

---

## Architecture

```text
                    Knowledge Base
         (FAQs • Glossary • Regulations • PDFs)
                           │
                           ▼
          Ingestion Pipeline (Cleaning • Chunking)
                           │
                           ▼
                    Embedding Generation
                           │
                           ▼
                   Qdrant Vector Database
                           │
                           ▼
                    Semantic Retriever
                           │
                           ▼
               Prompt + Retrieved Context
                           │
                           ▼
               Gemini / OpenAI (LLM Layer)
                           │
                           ▼
                  FastAPI REST Backend
                           │
                           ▼
                  Next.js + React Client
```

---

## Project Structure

```text
health-knowledge-assistant/

├── backend/
│   ├── src/
│   │   ├── api/
│   │   ├── ingestion/
│   │   ├── rag/
│   │   └── utils/
│   ├── scripts/
│   └── data/
│
├── frontend/
│   ├── app/
│   ├── components/
│   └── services/
│
└── README.md
```

---

## RAG Workflow

```text
Documents
   ↓
Chunking
   ↓
Embeddings
   ↓
Qdrant
   ↓
Retriever
   ↓
LLM
   ↓
Answer + Sources
```

---

## API

**POST** `/chat`

```json
{
  "question": "How does health insurance affiliation work?"
}
```

```json
{
  "answer": "...",
  "sources": [
    {
      "source": "faq_health.json"
    }
  ]
}
```

---

## Quick Start

### Backend

```bash
cd backend

pip install -r requirements.txt

uvicorn src.api.main:app --reload
```

API documentation:

```text
http://localhost:8000/docs
```

### Frontend

```bash
cd frontend

npm install

npm run dev
```

---

## Environment Variables

Backend

```env
OPENAI_API_KEY=
GEMINI_API_KEY=
LLM_PROVIDER=gemini
```

Frontend

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Roadmap

* Conversation memory
* Hybrid search
* Streaming responses
* Docker deployment
* Authentication
* Cloud vector database

---

## License

This project is intended for educational and portfolio purposes. Responses are generated from curated healthcare knowledge sources and should not replace professional medical advice.
