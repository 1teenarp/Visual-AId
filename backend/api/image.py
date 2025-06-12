from fastapi import APIRouter, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse
from backend.models.ollama_client import analyze_with_image
import base64

router = APIRouter()

@router.post("/analyze-image")
async def analyze_image(
    file: UploadFile = File(...),
    prompt: str = Form("Describe the image")
):
    try:
        image_bytes = await file.read()
        result = analyze_with_image(prompt, image_bytes)
        return JSONResponse(content={"result": result})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@router.post("/capture-frame")
async def capture_frame(request: Request):
    try:
        data = await request.json()
        img_b64 = data.get("image_base64")
        prompt = data.get("prompt", "What do you see?")

        if not img_b64:
            return JSONResponse(status_code=400, content={"error": "Missing base64 image"})

        image_bytes = base64.b64decode(img_b64)
        result = analyze_with_image(prompt, image_bytes)

        return JSONResponse(content={"result": result})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
