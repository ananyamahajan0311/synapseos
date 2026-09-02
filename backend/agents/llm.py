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
You are the document-generation assistant for SynapseOS.

The user wants to create a document.

USER REQUEST:
{prompt}

Understand the user's request and generate the ACTUAL content
they requested.

Do not merely repeat, summarize, or describe the request.

Follow all requirements specified by the user, including:
- topic
- quantity
- format
- structure
- difficulty
- language
- answers
- examples
- length
- any other constraints

If the user asks for multiple items, generate all requested items.
If the user specifies a number, produce exactly that number.

Use clear headings, numbering, paragraphs, and bullet points
where appropriate.

Formatting rules:
- Use # for major section headings.
- Put each heading on its own line.
- Use paragraphs for normal content.
- Use "- " for bullet points when appropriate.
- Do not use Markdown code blocks.
- Return ONLY the content that belongs in the document.
- Do not explain your process.

Generate the final document content now.
""",
    )

    return response.text

def generate_email(prompt):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"""
You are the email-writing assistant for SynapseOS.

The user wants to send an email.

USER REQUEST:
{prompt}

Your task:
- Understand what the user wants to communicate.
- Write the actual email.
- Create an appropriate subject.
- Keep the email professional and natural.
- Follow the user's requested tone, length, and purpose.

Return ONLY this exact format:

SUBJECT: <email subject>

BODY:
<complete email body>

Do not add explanations.
Do not use Markdown code blocks.
""",
    )

    return response.text

def generate_meeting_details(email_text):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"""
You are the meeting extraction assistant for SynapseOS.

Read the email below and determine whether it contains
a meeting/event that should be added to Google Calendar.

EMAIL:
{email_text}

Extract:
- meeting title
- date
- start time
- duration in minutes

Return ONLY this exact format:

TITLE: <meeting title>
DATE: <date>
TIME: <start time>
DURATION: <duration in minutes>

If a value cannot be determined, write:
UNKNOWN

Do not explain your reasoning.
Do not use Markdown.
""",
    )

    return response.text
def summarize_emails(email_text):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"""
You are the email summarization assistant for SynapseOS.

The following text contains emails retrieved from the user's Gmail.

EMAILS:
{email_text}

Summarize the emails clearly and concisely.

Include:
- The main topic
- Important dates and times
- Important people or senders
- Important actions or decisions
- Any other important information

If there are multiple emails, combine related information
and avoid unnecessary repetition.

Use simple, easy-to-read language.

Return ONLY the summary.
Do not explain your reasoning.
Do not mention that you are an AI.
""",
    )

    return response.text