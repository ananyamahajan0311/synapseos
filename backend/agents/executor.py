from tools.calculator import calculate
from tools.datetime_tool import get_datetime
from tools.browser import open_google
from agents.chat_agent import chat_with_ai
from tools.calendar_tool import create_event

class Executor:

    def execute(self, plan, context=""):
        tool = plan.get("tool", "chat")
        tool_input = plan.get("input", "")

        if tool == "calculator":
            return calculate(tool_input)

        elif tool == "datetime":
            return get_datetime()

        elif tool == "browser":
            return open_google(tool_input)

        elif tool == "chat":
            reply = chat_with_ai(context, tool_input)

        elif tool == "calendar":
            return create_event(tool_input)

            return {
                "status": "success",
                "message": reply
            }

        return {
            "status": "error",
            "message": f"Unknown tool: {tool}"
        }