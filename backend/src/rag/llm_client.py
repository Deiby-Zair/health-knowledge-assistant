import os
from pathlib import Path

from dotenv import load_dotenv

from backend.src.rag.schemas import LLMResponse

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

PROVIDER = os.getenv("LLM_PROVIDER", "gemini")

if PROVIDER == "openai":
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

elif PROVIDER == "gemini":
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate(prompt: str) -> LLMResponse:

    if PROVIDER == "openai":
        response = client.responses.parse(
            model="gpt-4.1-mini",
            input=prompt,
            text_format=LLMResponse,
        )

        return response.output_parsed

    elif PROVIDER == "gemini":
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL"),
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=LLMResponse,
                temperature=0.2,
            ),
        )

        return LLMResponse.model_validate_json(response.text)

    raise ValueError(f"Proveedor no soportado: {PROVIDER}")