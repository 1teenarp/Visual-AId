from fastapi import APIRouter, Request
from backend.models.ollama_client import analyze_with_image, analyze_with_text
from backend.utils.context_manager import get_context, add_to_context
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/chat")
async def chat(request: Request):
    data = await request.json()
    client_id = data.get("client_id", "default")
    prompt = data.get("prompt", "")

    if not prompt:
        return JSONResponse(status_code=400, content={"error": "Prompt required"})

    # Build conversation string
    context = get_context(client_id)
    full_prompt = "\n".join(
        f"{m['role'].capitalize()}: {m['message']}" for m in context
    ) + f"\nUser: {prompt}"

    # Query model
    reply = analyze_with_text(full_prompt)

    # Update context
    add_to_context(client_id, "user", prompt)
    add_to_context(client_id, "assistant", reply)

    return {"response": reply, "history": get_context(client_id)}
