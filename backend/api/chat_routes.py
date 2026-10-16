
import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from google.genai import errors

from api.schemas import PromptRequest
from agents.planner import Planner
from agents.executor import Executor
from memory import Memory
from agents.plan_validator import validate_plan, PlanValidationError

router = APIRouter(tags=["Chat"])

logger = logging.getLogger(__name__)

planner = Planner()
executor = Executor()
memory = Memory()


@router.post("/chat")
def chat(data: PromptRequest):
    try:
        memory.add("User", data.prompt)
        context = memory.get_context()

        plan = validate_plan(planner.plan(data.prompt))
        results = executor.execute(plan, context)

        assistant_reply = "\n\n".join(
            item.get("message", "")
            for item in results
        )

        memory.add("Assistant", assistant_reply)

        return {
            "status": "success",
            "message": data.prompt,
            "plan": plan,
            "results": results,
        }

    except errors.ServerError as exc:
        status_code = getattr(exc, "status_code", None)

        if status_code in (500, 502, 503, 504):
            logger.warning(
                "Gemini temporarily unavailable (HTTP %s).",
                status_code,
            )
            return JSONResponse(
                status_code=503,
                content={
                    "status": "error",
                    "message": (
                        "SynapseOS's AI service is temporarily unavailable. "
                        "Please try again shortly. Check your email drafts "
                        "before retrying an email request."
                    ),
                    "plan": [],
                    "results": [],
                },
            )

        logger.exception("Gemini server error while processing chat.")
        return JSONResponse(
            status_code=502,
            content={
                "status": "error",
                "message": "The AI service could not complete your request.",
                "plan": [],
                "results": [],
            },
        )
    except PlanValidationError as exc:
        logger.warning("Rejected invalid execution plan: %s", exc)
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "The requested execution plan was invalid.",
                "plan": [],
                "results": [],
            },
        )
    except Exception:
        logger.exception("Unexpected error while processing chat.")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": (
                    "SynapseOS could not complete your request. "
                    "Please try again."
                ),
                "plan": [],
                "results": [],
            },
        )
