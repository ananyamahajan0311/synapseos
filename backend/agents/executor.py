import re
from tools.calculator import calculate
from tools.datetime_tool import get_datetime
from tools.browser import open_google

from tools.calendar_tool import (
    create_event,
    create_event_from_email
)

from agents.chat_agent import chat_with_ai
from agents.llm import (
    generate_content,
    generate_email,
    generate_meeting_details,
    summarize_emails
)

from tools.calendar_list import list_events
from tools.calendar_delete import delete_event

from tools.gmail_read import read_emails
from tools.gmail_send import send_email
from tools.gmail_search import search_emails
from tools.gmail_parser import parse_email_command

from tools.docs_create import create_document
from tools.docs_list import list_documents

from tools.sheets_create import create_sheet


class Executor:

    def execute(self, plans, context=""):

        results = []

        spreadsheet_url = None
        calendar_url = None
        document_url = None

        # Stores Gmail output so another tool
        # can use the email content.
        email_content = None

        for plan in plans:

            tool = plan.get("tool", "chat")
            tool_input = plan.get("input", "")

            print("\n========== EXECUTING TOOL ==========")
            print("Tool:", tool)
            print("Input:", tool_input)

            # ==================================================
            # CALCULATOR
            # ==================================================

            if tool == "calculator":

                result = calculate(tool_input)

            # ==================================================
            # DATE & TIME
            # ==================================================

            elif tool == "datetime":

                result = get_datetime()

            # ==================================================
            # BROWSER
            # ==================================================

            elif tool == "browser":

                result = open_google(tool_input)

            # ==================================================
            # CALENDAR CREATE
            # ==================================================

            elif tool == "calendar_create":

                result = create_event(tool_input)

                if result.get("status") == "success":

                    # Prefer the direct URL returned by the tool
                    calendar_url = result.get("calendar_url")

                    # Fallback: extract URL from message
                    if not calendar_url:

                        message = result.get("message", "")

                        for line in message.splitlines():

                            if line.startswith("🔗"):

                                calendar_url = (
                                    line.replace(
                                        "🔗",
                                        ""
                                    ).strip()
                                )

                                break

            # ==================================================
            # CALENDAR CREATE FROM EMAIL
            # ==================================================

            elif tool == "calendar_create_from_email":
                print("\n========== CALENDAR FROM EMAIL ==========")
                print("Email content received:")
                print(email_content)
                # Use Gmail result if available
                if email_content:

                    result = create_event_from_email(
                        email_content
                    )

                    print("\nCalendar result:")
                    print(result)

                    if result.get("status") == "success":

                        calendar_url = result.get(
                            "calendar_url"
                        )

                else:

                    result = {
                        "status": "error",
                        "message": (
                            "No email content available "
                            "for calendar creation."
                        )
                    }
                    print(result)
            # ==================================================
            # CALENDAR LIST
            # ==================================================

            elif tool == "calendar_list":

                result = list_events()

            # ==================================================
            # CALENDAR DELETE
            # ==================================================

            elif tool == "calendar_delete":

                result = delete_event(tool_input)

            # ==================================================
            # CHAT
            # ==================================================

            elif tool == "chat":

                result = {
                    "status": "success",
                    "message": chat_with_ai(
                        context,
                        tool_input
                    )
                }

            # ==================================================
            # GMAIL READ
            # ==================================================

            elif tool == "gmail_read":
                max_results = 5
                if tool_input:
                    try:
                        max_results = int(tool_input)
                    except ValueError:
                        max_results = 5
                
                result = read_emails(
                    max_results=max_results
                    )

    # Save email content for another tool
                if result.get("status") == "success":
                    email_content = result.get(
                          "message",
            ""
        )

            # ==================================================
            # GMAIL SEARCH
            # ==================================================

            elif tool == "gmail_search":

                result = search_emails(tool_input)

                print("\n========== GMAIL SEARCH RESULT ==========")
                
                print(result)

                if result.get("status") == "success":

                     email_content = result.get("message", "")
                     print("\n========== EMAIL CONTENT SAVED ==========")
                     print(email_content)

            elif tool == "email_summarize":
                if email_content:
                    summary = summarize_emails(
                       email_content
                       )
                    result = {
            "status": "success",
            "message": summary
        }
                else:
                    result = {
            "status": "error",
            "message": (
                "No email content available "
                "to summarize."
            )
        }

            # ==================================================
            # GMAIL SEND
            # ==================================================

            elif tool == "gmail_send":

                print(
                    "\n========== EXECUTING GMAIL =========="
                )

                print(
                    "Tool input:",
                    tool_input
                )

                # Extract recipient from the user's request
                email = parse_email_command(
                    tool_input
                )

                print(
                    "Recipient:",
                    email["to"]
                )

                # Generate subject and body using Gemini
                if spreadsheet_url:
                     email_prompt = f"""
The user wants to send an email.

USER REQUEST:
{tool_input}

A Google Spreadsheet has already been created successfully.

SPREADSHEET URL:
{spreadsheet_url}

Write a short professional email to the requested recipient.

IMPORTANT:
- Do NOT recreate or list the MCQs in the email.
- Do NOT generate spreadsheet content again.
- Tell the recipient that the requested spreadsheet has been created.
- Include the spreadsheet URL exactly as provided above.
- Return the email using the normal SUBJECT and BODY format.
"""
                else:
                      email_prompt = tool_input
                generated_email = generate_email(
    email_prompt
)

                print(
                    "Generated email:",
                    generated_email
                )

                # Extract subject
                subject_match = re.search(
                    r"SUBJECT:\s*(.*)",
                    generated_email,
                    re.IGNORECASE
                )

                subject = ""

                if subject_match:
                    subject = subject_match.group(1).strip()

                # Extract body
                body_match = re.search(
                    r"BODY:\s*(.*)",
                    generated_email,
                    re.IGNORECASE | re.DOTALL
                )

                body = ""

                if body_match:
                    body = body_match.group(1).strip()

                # Fallback to the original parsed values
                if not subject:
                    subject = email["subject"]

                if not body:
                    body = email["body"]

                # Make sure recipient exists
                if not email["to"]:

                    result = {
                        "status": "error",
                        "message": (
                            "I need a recipient email address "
                            "to send the email."
                        )
                    }

                else:

                    result = send_email(
                        email["to"],
                        subject,
                        body
                    )

                    print(
                        "Gmail result:",
                        result
                    )
            # ==================================================
            # GOOGLE DOCS CREATE
            # ==================================================

            elif tool == "docs_create":

                result = create_document(
                    tool_input
                )

                if result.get("status") == "success":

                    document_url = result.get(
                        "message",
                        ""
                    ).splitlines()[-1]

            # ==================================================
            # GOOGLE DOCS LIST
            # ==================================================

            elif tool == "docs_list":

                result = list_documents()

            # ==================================================
            # GOOGLE SHEETS CREATE
            # ==================================================

            elif tool == "sheets_create":
                result = create_sheet(tool_input)
                if result.get("status") == "success":
                    spreadsheet_url = result.get("url")

                
            # ==================================================
            # UNKNOWN TOOL
            # ==================================================

            else:

                result = {
                    "status": "error",
                    "message": (
                        f"Unknown tool: {tool}"
                    )
                }

            results.append(result)

        return results