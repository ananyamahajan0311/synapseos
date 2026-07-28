from tools.calculator import calculate
from tools.datetime_tool import get_datetime
from tools.browser import open_google


class Executor:

    def execute(self, plan):

        tool = plan["tool"]

        if tool == "calculator":
            return calculate(plan["input"])

        if tool == "datetime":
            return get_datetime()

        if tool == "browser":
            return open_google()

        return {
            "status": "success",
            "message": "No tool required."
        }