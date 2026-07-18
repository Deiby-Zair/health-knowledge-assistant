import os
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("LLM_PROVIDER", "gemini")

if PROVIDER == "openai":
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

elif PROVIDER == "gemini":
    from google import genai
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate(prompt: str) -> str:
    if PROVIDER == "openai":
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return response.choices[0].message.content

    elif PROVIDER == "gemini":
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text