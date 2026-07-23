from fastapi import FastAPI
from pydantic import BaseModel

from backend.src.rag.rag_chain import ask

app = FastAPI()

class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
def chat(request: ChatRequest):
    answer = ask(request.question)

    return {
        "answer": answer["answer"],
        "sources": answer["sources"]
    }