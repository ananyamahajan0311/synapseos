import json
from agents.llm import generate_plan


class Planner:

    def __init__(self):
        with open("prompts/planner_prompt.txt", "r", encoding="utf-8") as f:
            self.system_prompt = f.read()

    def plan(self, prompt):
        response = generate_plan(prompt, self.system_prompt)

        # Clean Gemini output
        response = (
            response.replace("```json", "")
            .replace("```", "")
            .strip()
        )

        try:
            plan = json.loads(response)

            # Convert single object into list
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