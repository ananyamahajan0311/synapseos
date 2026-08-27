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

        text = prompt.lower()

        # ============================================================
        # EMAIL + CALENDAR WORKFLOW
        # Example:
        # "Mail my friend about meeting tomorrow at 3 pm
        #  and schedule it on my calendar"
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

        if "calculate" in text or any(
            op in text for op in ["+", "-", "*", "/"]
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

        if "time" in text or "date" in text:
            return [
                {
                    "tool": "datetime",
                    "input": ""
                }
            ]

        # ============================================================
        # CALENDAR LIST
        # ============================================================

        if (
            "show my calendar" in text
            or "upcoming events" in text
            or "my calendar" in text
        ):
            return [
                {
                    "tool": "calendar_list",
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
        ):
            return [
                {
                    "tool": "calendar_delete",
                    "input": prompt
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
        ):
            return [
                {
                    "tool": "calendar_create",
                    "input": prompt
                }
            ]
        # ---------------- Gmail Search ----------------
        if (
            "search email" in text
            or "search emails" in text
            or "search my emails" in text
            or "find email" in text
            or "find emails" in text
            or "emails from" in text
            or "emails about" in text
        ):
             return [{
        "tool": "gmail_search",
        "input": prompt
    }]

        # ============================================================
        # BROWSER
        # ============================================================

        if "search" in text or "open" in text:
            return [
                {
                    "tool": "browser",
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
            or "inbox" in text
            or "unread emails" in text
        ):
            return [
                {
                    "tool": "gmail_read",
                    "input": ""
                }
            ]

        # ============================================================
        # GMAIL SEARCH
        # ============================================================

        if (
            "search email" in text
            or "search emails" in text
            or "find email" in text
            or "find emails" in text
            or "emails from" in text
            or "emails about" in text
        ):
            return [
                {
                    "tool": "gmail_search",
                    "input": prompt
                }
            ]

        # ============================================================
        # SHEETS + GMAIL
        # ============================================================

        if (
            "spreadsheet" in text
            and
            (
                "email it" in text
                or "email the" in text
                or "send it" in text
            )
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
        # GMAIL SEND
        # ============================================================

        if (
            "send email" in text
            or "send an email" in text
            or "compose email" in text
            or "email " in text
            or text.startswith("mail ")
        ):
            return [
                {
                    "tool": "gmail_send",
                    "input": prompt
                }
            ]

        # ============================================================
        # GOOGLE DOCS
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