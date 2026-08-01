from fastapi import APIRouter
import traceback

from api.schemas import PromptRequest
from agents.planner import Planner
from agents.executor import Executor
from memory import Memory

router = APIRouter(tags=["Chat"])

planner = Planner()
executor = Executor()
memory = Memory()


@router.post("/chat")
def chat(data: PromptRequest):
    try:
        # Store the user's message
        memory.add("User", data.prompt)

        # Get conversation history
        context = memory.get_context()

        print("\n========== MEMORY ==========")
        print(context)
        print("============================\n")

        # Send the conversation context to Gemini
        plan = planner.plan(context)

        print("PLAN:", plan)

        # Execute the selected tool
        result = executor.execute(plan, context)

        print("RESULT:", result)

        # Save the assistant's reply
        memory.add(
            "Assistant",
            result.get("message", "")
        )

        return {
            "status": "success",
            "message": data.prompt,
            "plan": plan,
            "result": result
        }

    except Exception:
        print("\n========== CHAT ERROR ==========")
        traceback.print_exc()
        print("================================\n")

        return {
            "status": "error",
            "message": "Failed to process request.",
            "plan": {},
            "result": {
                "message": "Something went wrong."
            }
        }