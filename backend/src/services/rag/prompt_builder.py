from textwrap import dedent

MAX_CONTEXT_CHARS = 12000


def build_prompt(question: str, context: str) -> str:
    """
    Construye el prompt enviado al LLM.

    Parameters
    ----------
    question : str
        Pregunta del usuario.
    context : str
        Contexto recuperado desde Qdrant.
    """

    context = context.strip()

    if len(context) > MAX_CONTEXT_CHARS:
        context = context[:MAX_CONTEXT_CHARS]

    if context:
        context_section = f"""
CONTEXTO RECUPERADO
------------------
{context}
"""
    else:
        context_section = """
CONTEXTO RECUPERADO
------------------
No se recuperó información relevante de la base de conocimiento.
"""

    return dedent(
        f"""
Eres un asistente especializado en información del Ministerio de Salud y Protección Social de Colombia.

## Objetivo

    Responde únicamente preguntas relacionadas con el sistema de salud colombiano utilizando prioritariamente el contexto recuperado.

    ## Reglas

    1. Si el contexto contiene la respuesta, responde basándote únicamente en él.
    2. Si el contexto es insuficiente pero conoces la respuesta con alta certeza, indícalo explícitamente diciendo que la respuesta no proviene del contexto recuperado.
    3. Si no conoces la respuesta, indícalo claramente.
    4. No inventes información.
    5. No cites documentos ni inventes fuentes.
    6. No expliques cómo funciona el sistema RAG.
    7. Responde siempre en español.
    8. Si la pregunta no está relacionada con el sistema de salud colombiano, indícalo amablemente y no respondas la consulta.

{context_section}

PREGUNTA
---------
{question}

Devuelve únicamente un objeto JSON con el formato esperado.
"""
    ).strip()