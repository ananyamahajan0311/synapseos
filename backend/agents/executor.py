from tools.calculator import calculate
from tools.datetime_tool import get_datetime
from tools.browser import open_google
from tools.calendar_tool import create_event
from agents.chat_agent import chat_with_ai
from tools.calendar_list import list_events

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
            elif tool == "calendar_list":
                result = list_events()

            else:
                result = {
                    "status": "error",
                    "message": f"Unknown tool: {tool}"
                }

            results.append(result)

        return results