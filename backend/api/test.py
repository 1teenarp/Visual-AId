import cv2
import base64
import requests
import time, json

cap = cv2.VideoCapture(0)

# Warm up camera
for _ in range(5):
    cap.read()
    time.sleep(0.1)

ret, frame = cap.read()
cap.release()

if not ret:
    raise RuntimeError("Failed to capture frame from webcam")

_, img_encoded = cv2.imencode('.jpg', frame)
img_b64 = base64.b64encode(img_encoded.tobytes()).decode('utf-8')

response = requests.post("http://localhost:8000/capture-frame", json={
    "image_base64": img_b64,
    "prompt": "Enumerate any objects you see and race, ethnicity, gender and mood of the persons you see, returning a JSON of objects and persons."
})

print(response.json())

print(json.dumps(response.json().get("result"), indent=4))
