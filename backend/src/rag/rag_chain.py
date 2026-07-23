from backend.src.rag.retriever import retrieve_context
from backend.src.rag.llm_manager import generate_response


def ask(question: str):

    # Recuperar contexto
    context, sources = retrieve_context(
        question,
        limit=10,
    )

    prompt = f"""
Eres un asistente del sistema de salud colombiano.

Responde apoyándote mayoritariamente en el contexto proporcionado.

Si no encuentras la respuesta, indica claramente que respondes fuera del contexto RAG.

Responde únicamente aspectos relacionados con el sistema de salud colombiano.

CONTEXTO:
{context}

PREGUNTA:
{question}
"""

    response = generate_response(prompt)

    if response.success:

        return {
            "success": True,
            "answer": response.answer,
            "sources": sources,
        }

    return {
        "success": False,
        "answer": (
            "No fue posible generar una respuesta en este momento. "
            "El servicio de IA se encuentra temporalmente no disponible. "
            "Intenta nuevamente en unos segundos."
        ),
        "sources": sources,
        "error": response.error,
    }