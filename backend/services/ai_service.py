from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


class AIService:
    def generate_email(self, prompt: str):

        # Temporary implementation
        return f"""Subject: Generated Email

Hello,

This is a demo email generated for:

{prompt}

Thank you.

Regards,
SynapseOS
"""