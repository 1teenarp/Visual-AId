from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import tempfile
from backend.voice.stt import transcribe_audio

router = APIRouter()

@router.post("/stt")
async def stt(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp.flush()
            transcript = transcribe_audio(tmp.name)

        return {"transcript": transcript}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
