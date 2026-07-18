from src.retriever import retrieve_context
from src.llm_client import generate

def ask(question: str):
    # Recuperar contexto desde Qdrant
    context, sources = retrieve_context(question, limit=10)

    prompt = f"""
    Eres un asistente del sistema de salud colombiano.
    Responde apoyandote mayoritariamenteen el contexto proporcionado.
    Si no encuentras la respuesta, indíca claramente que respondes fuera del contexto RAG.
    Responde unicamente a aspectos relacionados con el sistema de salud colombiano.

    CONTEXTO:
    {context}

    PREGUNTA:
    {question}
    """

    answer = generate(prompt)

    return {
        "answer": answer,
        "sources": sources
    }