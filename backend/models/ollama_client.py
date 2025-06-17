import requests
import base64
from typing import Optional

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5vl:3b"  # or whatever tag you've assigned

def analyze_with_image(prompt: str, image_bytes: Optional[bytes] = None) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    if image_bytes:
        encoded_image = base64.b64encode(image_bytes).decode('utf-8')
        payload["images"] = [encoded_image]

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        return f"[Error querying model: {str(e)}]"

def analyze_with_text(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        return f"[Error querying model: {str(e)}]"
