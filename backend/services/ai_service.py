
import os
import logging

from google import genai
from dotenv import load_dotenv
from google.api_core import exceptions as google_exceptions

load_dotenv()

logger = logging.getLogger(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY) if API_KEY else None


class AIService:
    def generate_email(self, prompt: str):
        if not API_KEY or client is None:
            raise RuntimeError(
                "Gemini is not configured. Please check GEMINI_API_KEY."
            )

        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Please enter a prompt.")

        # Temporary implementation retained intentionally.
        # Replace this with a Gemini API call when AI generation is enabled.
        return f"""Subject: Generated Email

Hello,

This is a demo email generated for:

{prompt.strip()}

Thank you.

Regards,
SynapseOS
"""
