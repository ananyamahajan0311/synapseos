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

class Executor:

    def execute(self, plans, context=""):

        results = []

        for plan in plans:

            tool = plan.get("tool", "chat")
            tool_input = plan.get("input", "")

            if tool == "calculator":
                result = calculate(tool_input)

            elif tool == "datetime":
                result = get_datetime()

            elif tool == "browser":
                result = open_google(tool_input)

            elif tool == "calendar_create":
                result = create_event(tool_input)

            elif tool == "calendar_list":
                result = list_events()

            elif tool == "chat":
                result = {
                    "status": "success",
                    "message": chat_with_ai(context, tool_input)
                }
            
            elif tool == "calendar_delete":
                result = delete_event(tool_input)

            elif tool == "gmail_read":
                result = read_emails()

            elif tool == "gmail_search":
                result = search_emails(tool_input)

            elif tool == "gmail_send":
                email = parse_email_command(tool_input)
                result = send_email(
                    email["to"],
                    email["subject"],
                    email["body"]
                    )

            elif tool == "docs_create":
                result = create_document(tool_input)

            elif tool == "docs_list":
                result = list_documents()

            else:
                result = {
                    "status": "error",
                    "message": f"Unknown tool: {tool}"
                }


            results.append(result)

        return results