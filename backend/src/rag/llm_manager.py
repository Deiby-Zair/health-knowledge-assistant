from __future__ import annotations

import logging
import time
from dataclasses import dataclass

from backend.src.rag.llm_client import generate

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class LLMResponse:
    success: bool
    answer: str | None = None
    error: str | None = None
    retries: int = 0


def generate_response(
    prompt: str,
    *,
    max_retries: int = 3,
    retry_delay: float = 2.0,
) -> LLMResponse:
    """
    Gestiona las llamadas al LLM aplicando:
    - Reintentos
    - Logging
    - Respuesta uniforme
    """

    last_error = None

    for attempt in range(max_retries):

        try:

            answer = generate(prompt)

            return LLMResponse(
                success=True,
                answer=answer,
                retries=attempt,
            )

        except Exception as exc:

            last_error = exc

            logger.warning(
                "Intento %s/%s falló: %s",
                attempt + 1,
                max_retries,
                exc,
            )

            if attempt < max_retries - 1:
                time.sleep(retry_delay)

    logger.exception("No fue posible obtener respuesta del LLM.")

    return LLMResponse(
        success=False,
        error=str(last_error),
        retries=max_retries,
    )