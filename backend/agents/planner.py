import json
from agents.llm import generate_plan


class Planner:

    def __init__(self):
        with open("prompts/planner_prompt.txt", "r", encoding="utf-8") as f:
            self.system_prompt = f.read()

    def plan(self, prompt):
        text = prompt.lower()

        # ---------------- Calculator ----------------
        if "calculate" in text or any(
            op in text for op in ["+", "-", "*", "/"]
        ):
            return [{
                "tool": "calculator",
                "input": prompt
            }]

        # ---------------- Date & Time ----------------
        if "time" in text or "date" in text:
            return [{
                "tool": "datetime",
                "input": ""
            }]

        # ---------------- Calendar List ----------------
        if (
            "show my calendar" in text
            or "upcoming events" in text
            or "meetings" in text
        ):
            return [{
                "tool": "calendar_list",
                "input": ""
            }]

        # ---------------- Calendar + Gmail Workflow ----------------
        if (
            ("schedule" in text
             or "create event" in text
             or "meeting" in text)
            and
            ("email it" in text
             or "email the" in text
             or "send it" in text)
        ):
            return [
                {
                    "tool": "calendar_create",
                    "input": prompt
                },
                {
                    "tool": "gmail_send",
                    "input": prompt
                }
            ]

        # ---------------- Calendar Create ----------------
        if (
            "schedule" in text
            or "create event" in text
            or "add event" in text
        ):
            return [{
                "tool": "calendar_create",
                "input": prompt
            }]

        # ---------------- Calendar Delete ----------------
        if (
            "delete event" in text
            or "cancel meeting" in text
            or "remove event" in text
        ):
            return [{
                "tool": "calendar_delete",
                "input": prompt
            }]

        # ---------------- Browser ----------------
        if "search" in text or "open" in text:
            return [{
                "tool": "browser",
                "input": prompt
            }]

        # ---------------- Gmail Read ----------------
        if (
            "read my emails" in text
            or "latest emails" in text
            or "show my emails" in text
            or "show my inbox" in text
            or "inbox" in text
            or "unread emails" in text
        ):
            return [{
                "tool": "gmail_read",
                "input": ""
            }]

        # ---------------- Gmail Search ----------------
        if (
            "search email" in text
            or "search emails" in text
            or "find email" in text
            or "find emails" in text
            or "emails from" in text
            or "emails about" in text
        ):
            return [{
                "tool": "gmail_search",
                "input": prompt
            }]

        # ---------------- Sheets + Gmail Workflow ----------------
        if (
            "spreadsheet" in text
            and
            ("email it" in text
             or "email the" in text
             or "send it" in text)
        ):
            return [
                {
                    "tool": "sheets_create",
                    "input": prompt
                },
                {
                    "tool": "gmail_send",
                    "input": prompt
                }
            ]

        # ---------------- Docs + Gmail Workflow ----------------
        # IMPORTANT: This MUST come before Gmail Send.
        if (
            (
                "document" in text
                or "google doc" in text
                or "create a document" in text
                or "create document" in text
                or "create doc" in text
                or "new document" in text
            )
            and
            (
                "email" in text
                or "send" in text
            )
        ):
            return [
                {
                    "tool": "docs_create",
                    "input": prompt
                },
                {
                    "tool": "gmail_send",
                    "input": prompt
                }
            ]

        # ---------------- Gmail Send ----------------
        if (
            "send email" in text
            or "send an email" in text
            or "compose email" in text
            or "email " in text
        ):
            return [{
                "tool": "gmail_send",
                "input": prompt
            }]

        # ---------------- Google Docs ----------------
        if (
            "document" in text
            or "google doc" in text
            or "create a document" in text
            or "create document" in text
            or "create doc" in text
            or "new document" in text
        ):
            return [{
                "tool": "docs_create",
                "input": prompt
            }]

        # ---------------- Google Docs List ----------------
        if (
            "show my documents" in text
            or "list my documents" in text
            or "recent documents" in text
            or "my google docs" in text
            or "show my docs" in text
        ):
            return [{
                "tool": "docs_list",
                "input": ""
            }]

        # ---------------- Google Sheets ----------------
        if (
            "spreadsheet" in text
            or "sheet" in text
            or "google sheet" in text
            or "google spreadsheet" in text
        ):
            return [{
                "tool": "sheets_create",
                "input": prompt
            }]

        # ---------------- Gemini Fallback ----------------
        response = generate_plan(
            prompt,
            self.system_prompt
        )

        response = (
            response
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        try:
            plan = json.loads(response)

            if isinstance(plan, dict):
                plan = [plan]

            return plan

        except Exception:
            return [{
                "tool": "chat",
                "input": prompt
            }]