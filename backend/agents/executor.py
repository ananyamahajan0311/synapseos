from tools.calculator import calculate
from tools.datetime_tool import get_datetime
from tools.browser import open_google
from tools.calendar_tool import create_event
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

        for plan in plans:

            tool = plan.get("tool", "chat")
            tool_input = plan.get("input", "")

            # ---------------- Calculator ----------------
            if tool == "calculator":
                result = calculate(tool_input)

            # ---------------- Date & Time ----------------
            elif tool == "datetime":
                result = get_datetime()

            # ---------------- Browser ----------------
            elif tool == "browser":
                result = open_google(tool_input)

            # ---------------- Calendar Create ----------------
            elif tool == "calendar_create":

                result = create_event(tool_input)

                if result.get("status") == "success":

                    message = result.get("message", "")

                    for line in message.splitlines():

                        if line.startswith("🔗"):
                            calendar_url = line.replace(
                                "🔗", ""
                            ).strip()

                            # Only stop searching for the URL.
                            # Do NOT stop the main plan loop.
                            break

            # ---------------- Calendar List ----------------
            elif tool == "calendar_list":
                result = list_events()

            # ---------------- Calendar Delete ----------------
            elif tool == "calendar_delete":
                result = delete_event(tool_input)

            # ---------------- Chat ----------------
            elif tool == "chat":

                result = {
                    "status": "success",
                    "message": chat_with_ai(
                        context,
                        tool_input
                    )
                }

            # ---------------- Gmail Read ----------------
            elif tool == "gmail_read":
                result = read_emails()

            # ---------------- Gmail Search ----------------
            elif tool == "gmail_search":
                result = search_emails(tool_input)

            # ---------------- Gmail Send ----------------
            elif tool == "gmail_send":

                print("\n========== EXECUTING GMAIL ==========")
                print("Tool input:", tool_input)

                email = parse_email_command(tool_input)

                print("Parsed email:", email)

                # If a spreadsheet or calendar event
                # was created before this step,
                # include its link in the email.

                if spreadsheet_url or calendar_url:

                    if not email["subject"]:
                        email["subject"] = "SynapseOS Task Update"

                    email["body"] = (
                        "Hello,\n\n"
                        "The requested task has been completed "
                        "using SynapseOS.\n\n"
                    )

                    if spreadsheet_url:
                        email["body"] += (
                            f"Spreadsheet: {spreadsheet_url}\n\n"
                        )

                    if calendar_url:
                        email["body"] += (
                            f"Calendar Event: {calendar_url}\n\n"
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

                print("Gmail result:", result)

            # ---------------- Google Docs Create ----------------
            elif tool == "docs_create":
                result = create_document(tool_input)

            # ---------------- Google Docs List ----------------
            elif tool == "docs_list":
                result = list_documents()

            # ---------------- Google Sheets Create ----------------
            elif tool == "sheets_create":

                data = [
                    ["Project Task", "Status"],
                    [
                        "Complete SynapseOS backend",
                        "In Progress"
                    ],
                    [
                        "Integrate Google APIs",
                        "In Progress"
                    ],
                    [
                        "Test frontend",
                        "Pending"
                    ],
                    [
                        "Test Gmail integration",
                        "Pending"
                    ],
                    [
                        "Prepare project demo",
                        "Pending"
                    ]
                ]

                result = create_sheet(
                    "SynapseOS Project Tasks",
                    data
                )

                # Save the URL for the next tool
                if result.get("status") == "success":

                    spreadsheet_url = result.get(
                        "message",
                        ""
                    ).split("\n")[-1]

            # ---------------- Unknown Tool ----------------
            else:

                result = {
                    "status": "error",
                    "message": f"Unknown tool: {tool}"
                }

            results.append(result)

        return results