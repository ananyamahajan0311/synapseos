import re


class Planner:

    def plan(self, prompt):

        text = prompt.lower().strip()

        # Calculator (e.g. 2+2, 45 * 67)
        match = re.search(r"\d+\s*[\+\-\*/]\s*\d+", text)
        if match:
            return {
                "tool": "calculator",
                "input": match.group()
            }

        # Date / Time
        if any(word in text for word in ["date", "time", "today"]):
            return {
                "tool": "datetime"
            }

        # Browser
        if "open google" in text:
            return {
                "tool": "browser"
            }

        # Default
        return {
            "tool": "chat",
            "input": prompt
        }