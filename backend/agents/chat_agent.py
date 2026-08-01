import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def chat_with_ai(context, prompt):
    full_prompt = f"""
You are SynapseOS, an intelligent AI desktop assistant.

Below is the conversation history.

{context}

Current User Message:
{prompt}

Reply naturally and use the conversation history whenever it is helpful.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=full_prompt,
    )

    return response.text