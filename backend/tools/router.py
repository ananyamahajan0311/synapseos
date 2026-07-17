class ToolRouter:

    def run(self, plan):

        tool = plan.get("tool")

        if tool == "gmail":
            return {
                "status": "success",
                "message": "Mock Gmail tool executed."
            }

        if tool == "calendar":
            return {
                "status": "success",
                "message": "Mock Calendar tool executed."
            }

        if tool == "sheets":
            return {
                "status": "success",
                "message": "Mock Google Sheets tool executed."
            }

        return {
            "status": "success",
            "message": "No tool required."
        }