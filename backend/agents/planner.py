import json
from agents.llm import generate_plan


class Planner:

    def __init__(self):
        with open(
            "prompts/planner_prompt.txt",
            "r",
            encoding="utf-8"
        ) as f:
            self.system_prompt = f.read()

    def plan(self, prompt):

        text = prompt.lower().strip()

        # ============================================================
        # EMAIL SUMMARIZATION
        # ============================================================

        if (
            ("summarize" in text or "summary" in text)
            and
            ("email" in text or "emails" in text or "mail" in text)
        ):

            # One latest email
            if (
                "latest email" in text
                or "last email" in text
                or "most recent email" in text
            ):
                return [
                    {
                        "tool": "gmail_read",
                        "input": "1"
                    },
                    {
                        "tool": "email_summarize",
                        "input": prompt
                    }
                ]

            # Multiple latest emails
            return [
                {
                    "tool": "gmail_read",
                    "input": "5"
                },
                {
                    "tool": "email_summarize",
                    "input": prompt
                }
            ]

        # ============================================================
        # SHEETS + GMAIL
        # ============================================================
                
        if (
            ("spreadsheet" in text
             or "google sheet" in text
             or "google sheets" in text)
            and
            ("email" in text
             or "send" in text
             or "mail" in text)
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

        # ============================================================
        # GMAIL SEND
        # ============================================================

        if (
            "send an email" in text
            or "send email" in text
            or "compose email" in text
            or text.startswith("email ")
            or text.startswith("mail ")
        ):
            return [
                {
                    "tool": "gmail_send",
                    "input": prompt
                }
            ]

        # ============================================================
        # EMAIL + CALENDAR WORKFLOW
        # ============================================================

        if (
            ("email" in text or "mail" in text or "gmail" in text)
            and
            ("calendar" in text or "schedule" in text)
        ):
            return [
                {
                    "tool": "gmail_send",
                    "input": prompt
                },
                {
                    "tool": "calendar_create",
                    "input": prompt
                }
            ]

        # ============================================================
        # CALCULATOR
        # ============================================================

        if (
            "calculate" in text
            or "what is" in text and any(
                op in text for op in ["+", "-", "*", "/"]
            )
        ):
            return [
                {
                    "tool": "calculator",
                    "input": prompt
                }
            ]

        # ============================================================
        # DATE & TIME
        # ============================================================

        if (
            "what time" in text
            or "current time" in text
            or "today's date" in text
            or "current date" in text
            or text == "time"
            or text == "date"
        ):
            return [
                {
                    "tool": "datetime",
                    "input": ""
                }
            ]

        # ============================================================
        # CALENDAR DELETE
        # ============================================================

        if (
            "delete event" in text
            or "cancel meeting" in text
            or "remove event" in text
            or "delete meeting" in text
        ):
            return [
                {
                    "tool": "calendar_delete",
                    "input": prompt
                }
            ]

        # ============================================================
        # CALENDAR LIST
        # ============================================================

        if (
            "show my calendar" in text
            or "show calendar" in text
            or "upcoming events" in text
            or "my calendar" in text
            or "calendar events" in text
        ):
            return [
                {
                    "tool": "calendar_list",
                    "input": ""
                }
            ]

        # ============================================================
        # CALENDAR CREATE
        # ============================================================

        if (
            "schedule" in text
            or "create event" in text
            or "add event" in text
            or "add to my calendar" in text
            or "create a meeting" in text
        ):
            return [
                {
                    "tool": "calendar_create",
                    "input": prompt
                }
            ]

        # ============================================================
        # GMAIL READ
        # ============================================================

        if (
            "read my emails" in text
            or "latest emails" in text
            or "show my emails" in text
            or "show my inbox" in text
            or "show inbox" in text
            or text == "inbox"
            or "unread emails" in text
        ):
            return [
                {
                    "tool": "gmail_read",
                    "input": ""
                }
            ]

        

        # ============================================================
        # DOCS + GMAIL
        # ============================================================

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

        # ============================================================
        # GOOGLE DOCS LIST
        # ============================================================

        if (
            "show my documents" in text
            or "list my documents" in text
            or "recent documents" in text
            or "my google docs" in text
            or "show my docs" in text
        ):
            return [
                {
                    "tool": "docs_list",
                    "input": ""
                }
            ]

        # ============================================================
        # GOOGLE DOCS CREATE
        # ============================================================

        if (
            "document" in text
            or "google doc" in text
            or "create a document" in text
            or "create document" in text
            or "create doc" in text
            or "new document" in text
        ):
            return [
                {
                    "tool": "docs_create",
                    "input": prompt
                }
            ]

        # ============================================================
        # GOOGLE SHEETS
        # ============================================================

        if (
            "spreadsheet" in text
            or "google sheet" in text
            or "google spreadsheet" in text
        ):
            return [
                {
                    "tool": "sheets_create",
                    "input": prompt
                }
            ]

        # ============================================================
        # BROWSER
        # ============================================================

        if (
            "search web" in text
            or "search online" in text
            or "open website" in text
            or "open google" in text
        ):
            return [
                {
                    "tool": "browser",
                    "input": prompt
                }
            ]

        # ============================================================
        # GEMINI FALLBACK
        # ============================================================

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

            return [
                {
                    "tool": "chat",
                    "input": prompt
                }
            ]