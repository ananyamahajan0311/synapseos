from fastapi import APIRouter

from api.schemas import PromptRequest
from agents.planner import Planner
from agents.executor import Executor

router = APIRouter(tags=["Chat"])

planner = Planner()
executor = Executor()


@router.post("/chat")
def chat(data: PromptRequest):

    plan = planner.plan(data.prompt)

    result = executor.execute(plan)

    return {
        "message": data.prompt,
        "plan": plan,
        "result": result
    }