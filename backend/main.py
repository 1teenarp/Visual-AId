from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api import image, voice, chat  # Add chat when ready

app = FastAPI(title="Visual-AId")

# Allow all CORS origins for dev; tighten in prod
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/status")
def status():
    return {"status": "ok"}

# API routers
app.include_router(image.router)
app.include_router(voice.router)
app.include_router(chat.router)
