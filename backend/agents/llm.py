import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found.")

print("Loaded key:", api_key[:12] + "...")

client = genai.Client(api_key=api_key)


def generate_plan(prompt, system_prompt):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"{system_prompt}\n\nUser: {prompt}",
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    print("\n===== GEMINI RESPONSE =====")
    print(response.text)
    print("===========================\n")

    return response.text