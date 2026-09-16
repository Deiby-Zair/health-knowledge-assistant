from src.config import get_settings
from src.models.schemas import LLMResponse


def generate(prompt: str) -> LLMResponse:
    settings = get_settings()

    if settings.llm_provider == "openai":
        from openai import OpenAI

        client = OpenAI(api_key=settings.openai_api_key)

        response = client.responses.parse(
            model=settings.openai_model,
            input=prompt,
            text_format=LLMResponse,
        )

        return response.output_parsed

    if settings.llm_provider == "gemini":
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=settings.gemini_api_key)
        
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=LLMResponse,
                temperature=0.2,
            ),
        )

        return LLMResponse.model_validate_json(response.text)

    raise ValueError(
        f"Proveedor LLM no soportado: {settings.llm_provider}"
    )