let stream = null;
let isCameraOn = false;
const clientId = Math.random().toString(36).substring(2, 15);

const webcam = document.getElementById("webcam");
const frozenFrame = document.getElementById("frozenFrame");
const captureBtn = document.getElementById("captureBtn");
const startCamBtn = document.getElementById("startCam");
const promptInput = document.getElementById("prompt");
const loading = document.getElementById("loading");
const responseDisplay = document.getElementById("response");

function showLoading() {
  responseDisplay.textContent = "";
  loading.style.display = "block";
}

function hideLoading() {
  loading.style.display = "none";
}

// Toggle camera stream
async function toggleCamera() {
  if (!isCameraOn) {
    try {
      stream = await navigator.mediaDevices.getUserMedia({ video: true });
      webcam.srcObject = stream;
      webcam.style.display = "block";
      frozenFrame.style.display = "none";
      captureBtn.disabled = false;
      startCamBtn.textContent = "Stop Camera";
      isCameraOn = true;
    } catch (err) {
      alert("Failed to access webcam: " + err);
    }
  } else {
    stopCamera();
  }
}

// Stop and clean up the camera stream
function stopCamera() {
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
    stream = null;
  }
  isCameraOn = false;
  webcam.style.display = "none";
  captureBtn.disabled = true;
  startCamBtn.textContent = "Start Camera";
}

// Capture the frame and send to model
async function captureWebcam() {
  if (!isCameraOn) {
    alert("Camera is not active");
    return;
  }

  const canvas = document.createElement("canvas");
  canvas.width = webcam.videoWidth;
  canvas.height = webcam.videoHeight;
  const context = canvas.getContext("2d");
  context.drawImage(webcam, 0, 0, canvas.width, canvas.height);

  const imageDataUrl = canvas.toDataURL("image/jpeg");
  const base64Data = imageDataUrl.replace(/^data:image\/jpeg;base64,/, "");

  showLoading();
  stopCamera();
  frozenFrame.src = imageDataUrl;
  frozenFrame.style.display = "block";

  try {
    const res = await fetch("http://localhost:8000/capture-frame", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        image_base64: base64Data,
        prompt: promptInput.value || "What do you see?",
        client_id: clientId
      })
    });

    const result = await res.json();
    responseDisplay.textContent = result.result || result.error;
  } catch (err) {
    responseDisplay.textContent = "Error: " + err.message;
  } finally {
    hideLoading();
  }
}

// Upload and analyze static image
async function submitImage() {
  const fileInput = document.getElementById("imageInput");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select an image.");
    return;
  }

  showLoading();
  webcam.style.display = "none";
  frozenFrame.style.display = "block";
  frozenFrame.src = URL.createObjectURL(file);

  const formData = new FormData();
  formData.append("file", file);
  formData.append("prompt", promptInput.value || "Describe this image");
  formData.append("client_id", clientId);

  try {
    const res = await fetch("http://localhost:8000/analyze-image", {
      method: "POST",
      body: formData
    });

    const result = await res.json();
    responseDisplay.textContent = result.result || result.error;
  } catch (err) {
    responseDisplay.textContent = "Error: " + err.message;
  } finally {
    hideLoading();
  }
}


async function sendFollowup() {
  const prompt = document.getElementById("followupInput").value.trim();
  if (!prompt) return;

  showLoading();

  const res = await fetch("http://localhost:8000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      prompt: prompt,
      client_id: clientId
    })
  });

  const data = await res.json();
  hideLoading();
  renderHistory(data.history);
}

function renderHistory(history) {
  const container = document.getElementById("chatResponse");
  container.innerHTML = "";
  history.forEach(item => {
    const el = document.createElement("div");
    el.className = `msg ${item.role}`;
    el.textContent = `${item.role}: ${item.message}`;
    container.appendChild(el);
  });
}
