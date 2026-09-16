# 🩺 Health Knowledge Assistant

An AI-powered Retrieval-Augmented Generation (RAG) assistant that provides reliable information about the Colombian healthcare system using semantic search and Large Language Models (LLMs).

Built with a decoupled architecture featuring a **FastAPI backend**, **Next.js frontend**, and **Qdrant Cloud** as the vector database.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-009688)
![Next.js](https://img.shields.io/badge/Next.js-15-black)
![Qdrant](https://img.shields.io/badge/Qdrant-Cloud-red)
![License](https://img.shields.io/badge/License-Portfolio-lightgrey)

---

## Features

- 🔎 Retrieval-Augmented Generation (RAG)
- 🧠 Semantic search using vector embeddings
- 📖 Source-aware responses with document citations
- 🤖 Provider-agnostic LLM integration (Gemini & OpenAI)
- ☁️ Cloud-native vector database with Qdrant Cloud
- ⚡ FastAPI REST API
- 💬 Modern responsive chat interface built with Next.js
- 🏗️ Modular and scalable architecture
- 🔄 Automated document ingestion pipeline

---

## Tech Stack

| Backend | AI / RAG | Frontend |
|----------|----------|----------|
| Python | Google Gemini | Next.js |
| FastAPI | OpenAI | React |
| Uvicorn | Qdrant Cloud | TypeScript |
| Pydantic | Sentence Transformers | Tailwind CSS |
| python-dotenv | Prompt Engineering | Lucide React |

---

## Architecture

```text
                    Knowledge Base
        (FAQs • Glossary • Regulations • PDFs)
                           │
                           ▼
           Data Ingestion & Cleaning Pipeline
                           │
                           ▼
                  Text Chunk Generation
                           │
                           ▼
                 Embedding Generation
                           │
                           ▼
                 Qdrant Cloud Vector DB
                           │
                           ▼
                 Semantic Retrieval (RAG)
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
               Next.js + React Frontend
```

---

## Knowledge Base

The assistant retrieves information from curated Colombian healthcare documentation, including:

- Frequently Asked Questions (FAQs)
- Healthcare glossary
- Official healthcare documents
- PDF regulations and guidance
- Structured semantic chunks generated during preprocessing

Before serving user requests, documents are:

1. Cleaned and normalized
2. Split into semantic chunks
3. Converted into embeddings
4. Indexed in Qdrant Cloud
5. Retrieved through semantic similarity search

---

## Project Structure

```text
health-knowledge-assistant/
│
├── backend/
│   ├── src/
│   │   ├── api/
│   │   ├── ingestion/
│   │   ├── rag/
│   │   ├── llm/
│   │   └── utils/
│   │
│   ├── data/
│   │   ├── raw/
│   │   ├── processed/
│   │   └── chunks/
│   │
│   ├── requirements.txt
│   └── vercel.json
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── services/
│   ├── public/
│   └── vercel.json
│
└── README.md
```

---

## RAG Workflow

```text
Raw Documents
      │
      ▼
Document Processing
      │
      ▼
Text Chunking
      │
      ▼
Embedding Generation
      │
      ▼
Qdrant Cloud
      │
      ▼
Semantic Retrieval
      │
      ▼
LLM Generation
      │
      ▼
Answer + Sources
```

---

## API

### POST `/chat`

Request

```json
{
  "question": "How does health insurance affiliation work?"
}
```

Example Response

```json
{
  "success": true,
  "answer": "...",
  "confidence": 0.94,
  "used_rag": true,
  "sources": [
    {
      "title": "Health FAQ",
      "location": "faq_health.json",
      "score": 0.82
    }
  ]
}
```

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/Deiby-Zair/health-knowledge-assistant.git

cd health-knowledge-assistant
```

---

### 2. Backend

```bash
cd backend

python -m venv .venv

source .venv/bin/activate      # Linux / macOS

.venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

---

### 3. Build the Knowledge Base

Run the ingestion pipeline to process documents and populate the vector database.

```bash
python -m scripts.build_knowledge_base
```

---

### 4. Start the API

```bash
uvicorn src.api.main:app --reload
```

Swagger documentation:

```
http://localhost:8000/docs
```

---

### 5. Frontend

```bash
cd frontend

npm install

npm run dev
```

Open:

```
http://localhost:3000
```

---

## Environment Variables

### Backend

```env
OPENAI_API_KEY=

GEMINI_API_KEY=

LLM_PROVIDER=gemini

QDRANT_URL=

QDRANT_API_KEY=

QDRANT_COLLECTION=minsalud_rag
```

### Frontend

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Deployment

The application is deployed using a decoupled cloud architecture.

| Component | Platform |
|----------|----------|
| Frontend | Vercel |
| Backend | Vercel |
| Vector Database | Qdrant Cloud |

### Live Application

🔗 **Application**

https://health-knowledge-assistant-jz2og2brv-deibyzairs-projects.vercel.app/

---

## Future Improvements

- Conversation memory
- Streaming responses
- Hybrid search (semantic + keyword)
- Authentication
- Conversation history
- Multi-language support
- Additional healthcare datasets
- Evaluation metrics for retrieval quality

---

## Disclaimer

This project was developed for educational and portfolio purposes.

Although responses are generated using curated Colombian healthcare information and Retrieval-Augmented Generation (RAG), they may contain inaccuracies or become outdated over time.

Always consult official healthcare authorities or qualified medical professionals before making healthcare-related decisions.
