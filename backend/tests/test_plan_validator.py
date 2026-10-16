
import pytest

from agents.plan_validator import (
    PlanValidationError,
    validate_plan,
)


def test_legacy_plan_is_normalized():
    result = validate_plan([
        {"tool": "calculator", "input": "2+2"},
        {"tool": "datetime", "input": "today"},
    ])

    assert result[0]["id"] == "step_1"
    assert result[0]["depends_on"] == []
    assert result[1]["id"] == "step_2"


def test_explicit_dependencies_are_preserved():
    result = validate_plan([
        {"id": "create_doc", "tool": "docs_create", "input": "Report"},
        {
            "id": "prepare_email",
            "tool": "gmail_send",
            "input": "Email the report",
            "depends_on": ["create_doc"],
        },
    ])

    assert result[1]["depends_on"] == ["create_doc"]


def test_unknown_tool_is_rejected():
    with pytest.raises(PlanValidationError):
        validate_plan([{"tool": "delete_everything", "input": ""}])


def test_unknown_dependency_is_rejected():
    with pytest.raises(PlanValidationError):
        validate_plan([
            {
                "id": "step_a",
                "tool": "calculator",
                "input": "2+2",
                "depends_on": ["missing_step"],
            }
        ])


def test_dependency_cycle_is_rejected():
    with pytest.raises(PlanValidationError):
        validate_plan([
            {
                "id": "step_a",
                "tool": "calculator",
                "input": "2+2",
                "depends_on": ["step_b"],
            },
            {
                "id": "step_b",
                "tool": "datetime",
                "input": "today",
                "depends_on": ["step_a"],
            },
        ])


def test_empty_plan_is_rejected():
    with pytest.raises(PlanValidationError):
        validate_plan([])
