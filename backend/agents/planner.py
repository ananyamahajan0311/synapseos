class Planner:
    def plan(self, user_input: str):
        """
        Temporary rule-based planner.
        Later this will use an LLM.
        """

        text = user_input.lower()

        if "email" in text:
            return {
                "tool": "gmail",
                "action": "send_email"
            }

        if "calendar" in text:
            return {
                "tool": "calendar",
                "action": "create_event"
            }

        if "sheet" in text:
            return {
                "tool": "sheets",
                "action": "update_sheet"
            }

        return {
            "tool": None,
            "action": "chat"
        }