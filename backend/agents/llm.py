import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_plan(prompt, system_prompt):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"{system_prompt}\n\nUser: {prompt}",
    )
    return response.text


def generate_content(prompt):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"""
You are the document-writing assistant for SynapseOS.

Create well-structured content for the user's document request.

Formatting rules:
- Use # at the beginning of a line for major section headings.
- Put each heading on its own line.
- Put normal content below each heading as paragraphs.
- Use bullet points with "- " when appropriate.
- Do not use Markdown code blocks.
- Do not add explanations outside the requested document.
- Return only the document content.

Example:

# Introduction

Artificial intelligence is a field of computer science...

# Applications

- Healthcare
- Education
- Finance

# Conclusion

AI is transforming many industries.

User request:
{prompt}
""",
    )
    return response.text