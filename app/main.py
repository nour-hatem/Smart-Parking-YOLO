from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from ultralytics import YOLO
import cv2
import numpy as np
import io
import os

app = FastAPI(title="Smart Parking API")

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "model", "best.pt")
model = YOLO(MODEL_PATH)

def count_slots(results):
    empty, occupied = 0, 0
    for box in results[0].boxes:
        name = model.names[int(box.cls[0])]
        if name == "empty":
            empty += 1
        elif name == "occupied":
            occupied += 1
    return empty, occupied

def decode_image(file_bytes):
    arr = np.frombuffer(file_bytes, np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)

@app.post("/detect/json")
async def detect_json(file: UploadFile = File(...), conf: float = 0.4):
    image = decode_image(await file.read())
    results = model.predict(source=image, conf=conf, verbose=False)
    empty, occupied = count_slots(results)
    return JSONResponse({"empty": empty, "occupied": occupied, "total": empty + occupied})

@app.post("/detect/image")
async def detect_image(file: UploadFile = File(...), conf: float = 0.4):
    image = decode_image(await file.read())
    results = model.predict(source=image, conf=conf, verbose=False)
    annotated = results[0].plot()
    _, buffer = cv2.imencode(".jpg", annotated)
    return StreamingResponse(io.BytesIO(buffer.tobytes()), media_type="image/jpeg")

@app.post("/detect/full")
async def detect_full(file: UploadFile = File(...), conf: float = 0.4):
    image = decode_image(await file.read())
    results = model.predict(source=image, conf=conf, verbose=False)
    empty, occupied = count_slots(results)
    annotated = results[0].plot()
    _, buffer = cv2.imencode(".jpg", annotated)
    import base64
    encoded = base64.b64encode(buffer.tobytes()).decode("utf-8")
    return JSONResponse({
        "empty": empty,
        "occupied": occupied,
        "total": empty + occupied,
        "annotated_image": encoded
    })

@app.get("/health")
def health():
    return {"status": "ok"}