from tools.calculator import calculate
from tools.datetime_tool import get_datetime
from tools.browser import open_google


class Executor:

    def execute(self, plan):
        tool = plan.get("tool", "chat")
        tool_input = plan.get("input", "")

        if tool == "calculator":
            return calculate(tool_input)

        elif tool == "datetime":
            return get_datetime()

        elif tool == "browser":
            return open_google(tool_input)

        elif tool == "chat":
            return {
                "status": "success",
                "message": f"{tool_input}"
            }

        return {
            "status": "error",
            "message": f"Unknown tool: {tool}"
        }