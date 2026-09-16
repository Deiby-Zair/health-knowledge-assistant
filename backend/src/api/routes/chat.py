from fastapi import APIRouter
from pydantic import BaseModel

from src.services.rag.rag_chain import ask

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
def chat(request: ChatRequest):
    answer = ask(request.question)

    return {
        "answer": answer["answer"],
        "sources": answer["sources"],
    }