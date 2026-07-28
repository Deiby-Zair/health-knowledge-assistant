import logging

from src.rag.prompt_builder import build_prompt
from src.rag.retriever import retrieve_context
from src.rag.llm_manager import generate_response

logger = logging.getLogger(__name__)


def ask(question: str) -> dict:
    """
    Ejecuta el flujo RAG completo.

    Returns
    -------
    dict
        {
            success,
            answer,
            sources,
            used_rag,
            error
        }
    """

    question = question.strip()

    if not question:
        return {
            "success": False,
            "answer": "Debes ingresar una pregunta.",
            "sources": [],
            "used_rag": False,
            "error": "Empty question",
        }

    try:
        context, sources = retrieve_context(
            question=question,
            limit=5,
        )

    except Exception as e:
        logger.exception("Error recuperando contexto.")

        return {
            "success": False,
            "answer": (
                "No fue posible consultar la base de conocimiento en este momento."
            ),
            "sources": [],
            "used_rag": False,
            "error": str(e),
        }

    has_context = bool(context.strip())

    prompt = build_prompt(
        question=question,
        context=context,
    )

    try:
        response = generate_response(prompt)

    except Exception as e:
        logger.exception("Error llamando al proveedor LLM.")

        return {
            "success": False,
            "answer": (
                "No fue posible generar una respuesta en este momento. "
                "El servicio de IA se encuentra temporalmente no disponible."
            ),
            "sources": sources,
            "used_rag": has_context,
            "error": str(e),
        }

    if not response.success:
        return {
            "success": False,
            "answer": (
                "No fue posible generar una respuesta en este momento. "
                "El servicio de IA se encuentra temporalmente no disponible."
            ),
            "sources": sources,
            "used_rag": has_context,
            "error": response.error,
        }

    return {
        "success": True,
        "answer": response.answer.answer,
        "sources": sources,
        "used_rag": has_context,
        "error": None,
    }