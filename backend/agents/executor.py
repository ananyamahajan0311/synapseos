from tools.calculator import calculate
from tools.datetime_tool import get_datetime
from tools.browser import open_google

from tools.calendar_tool import (
    create_event,
    create_event_from_email
)

from agents.chat_agent import chat_with_ai

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

                result = read_emails()

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

                email = parse_email_command(
                    tool_input
                )

                print(
                    "Parsed email:",
                    email
                )

                # If another tool created something,
                # include its URL in the email.
                if (
                    spreadsheet_url
                    or calendar_url
                    or document_url
                ):

                    if not email["subject"]:

                        email["subject"] = (
                            "SynapseOS Task Update"
                        )

                    email["body"] = (
                        "Hello,\n\n"
                        "The requested task has been "
                        "completed using SynapseOS.\n\n"
                    )

                    if spreadsheet_url:

                        email["body"] += (
                            f"Spreadsheet: "
                            f"{spreadsheet_url}\n\n"
                        )

                    if calendar_url:

                        email["body"] += (
                            f"Calendar Event: "
                            f"{calendar_url}\n\n"
                        )

                    if document_url:

                        email["body"] += (
                            f"Google Document: "
                            f"{document_url}\n\n"
                        )

                    email["body"] += (
                        "Regards,\n"
                        "SynapseOS"
                    )

                result = send_email(
                    email["to"],
                    email["subject"],
                    email["body"]
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