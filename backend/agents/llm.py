import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_content(prompt):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"""
You are the document-writing assistant for SynapseOS.

Write high-quality, well-structured content for the user's document request.

Rules:
- Use clear section headings when appropriate.
- Use paragraphs and bullet points when useful.
- Do not add unnecessary explanations.
- Do not mention that you are an AI.
- Return only the document content.

User request:
{prompt}
""",
    )
    return response.text


def generate_content(prompt):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )
    return response.text