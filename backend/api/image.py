"""
Module: backend/api/image.py

Description: API endpoints for image analysis.

Endpoints:

* POST /analyze-image: Analyze an image with a given prompt.
* POST /capture-frame: Capture a frame from a video and analyze it.
"""

from fastapi import APIRouter, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse
from backend.models.ollama_client import analyze_with_image
import base64

router = APIRouter()

@router.post("/analyze-image")
async def analyze_image(
    file: UploadFile = File(...),
    prompt: str = Form("Describe the image"),
    client_id: str = Form(...)
):
    """
    Analyze an image with a given prompt.

    Args:
        file (UploadFile): The image to be analyzed.
        prompt (str): A description of the image. Defaults to "Describe the image".
        client_id (str): The ID of the client. Required.

    Returns:
        JSONResponse: A JSON response containing the analysis result.
    """
    from backend.utils.context_manager import reset_context, add_to_context
    try:
        reset_context(client_id)
        image_bytes = await file.read()
        result = analyze_with_image(prompt, image_bytes)
        return JSONResponse(content={"result": result})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@router.post("/capture-frame")
async def capture_frame(request: Request):
    """
    Capture a frame from a video and analyze it.

    Args:
        request (Request): The request containing the image data.

    Returns:
        JSONResponse: A JSON response containing the analysis result.
    """
    try:
        from backend.utils.context_manager import reset_context, add_to_context
        data = await request.json()
        img_b64 = data.get("image_base64")
        prompt = data.get("prompt", "What do you see?")
        client_id = data.get("client_id")

        if not img_b64:
            return JSONResponse(status_code=400, content={"error": "Missing base64 image"})

        if not client_id:
            return JSONResponse(status_code=400, content={"error": "Missing client_id"})

        reset_context(client_id)
        image_bytes = base64.b64decode(img_b64)
        result = analyze_with_image(prompt, image_bytes)

        return JSONResponse(content={"result": result})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})