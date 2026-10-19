
from typing import Any


ALLOWED_TOOLS = {
    "calculator",
    "datetime",
    "browser",
    "calendar_create",
    "calendar_create_from_email",
    "calendar_list",
    "calendar_delete",
    "chat",
    "gmail_read",
    "gmail_search",
    "gmail_send",
    "email_summarize",
    "docs_create",
        "docs_list",
    "docs_preview",
    "sheets_preview",
    "sheets_create",
}


class PlanValidationError(ValueError):
    pass


def validate_plan(plan: Any) -> list[dict]:
    if isinstance(plan, dict):
        plan = [plan]

    if not isinstance(plan, list) or not plan:
        raise PlanValidationError("The plan must contain at least one step.")

    if len(plan) > 20:
        raise PlanValidationError("The plan exceeds the 20-step limit.")

    validated = []
    seen_ids = set()

    for index, step in enumerate(plan, start=1):
        if not isinstance(step, dict):
            raise PlanValidationError(
                f"Step {index} must be a JSON object."
            )

        tool = step.get("tool")
        if not isinstance(tool, str) or tool not in ALLOWED_TOOLS:
            raise PlanValidationError(
                f"Step {index} contains an unsupported tool."
            )

        tool_input = step.get("input", "")
        if not isinstance(tool_input, str):
            raise PlanValidationError(
                f"Step {index} input must be a string."
            )

        step_id = step.get("id", f"step_{index}")
        if (
            not isinstance(step_id, str)
            or not step_id.strip()
            or step_id in seen_ids
        ):
            raise PlanValidationError(
                f"Step {index} has an invalid or duplicate ID."
            )

        dependencies = step.get("depends_on", [])
        if (
            not isinstance(dependencies, list)
            or any(not isinstance(dep, str) for dep in dependencies)
            or len(dependencies) != len(set(dependencies))
        ):
            raise PlanValidationError(
                f"Step {index} has invalid dependencies."
            )

        seen_ids.add(step_id)
        validated.append({
            "id": step_id,
            "tool": tool,
            "input": tool_input,
            "depends_on": dependencies,
        })

    ids = {step["id"] for step in validated}

    for step in validated:
        if step["id"] in step["depends_on"]:
            raise PlanValidationError(
                f"Step '{step['id']}' cannot depend on itself."
            )

        missing = set(step["depends_on"]) - ids
        if missing:
            raise PlanValidationError(
                f"Step '{step['id']}' has unknown dependencies."
            )

    # Detect dependency cycles.
    dependencies_by_id = {
        step["id"]: step["depends_on"] for step in validated
    }
    visiting = set()
    visited = set()

    def visit(step_id):
        if step_id in visiting:
            raise PlanValidationError(
                "The plan contains a dependency cycle."
            )

        if step_id in visited:
            return

        visiting.add(step_id)

        for dependency in dependencies_by_id[step_id]:
            visit(dependency)

        visiting.remove(step_id)
        visited.add(step_id)

    for step in validated:
        visit(step["id"])

    return validated


