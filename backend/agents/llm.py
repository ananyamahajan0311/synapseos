import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_plan(prompt, system_prompt):
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=f"{system_prompt}\n\nUser: {prompt}",
    )

    return response.text