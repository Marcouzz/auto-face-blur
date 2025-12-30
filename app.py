from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import uuid
import threading
from processor import anonymize_video

app = FastAPI()

os.makedirs("tmp", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

tasks = {}  #{"ready": False, "output": path}

@app.get("/", response_class=HTMLResponse)
def index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

def process_video(uid, input_path, output_path):
    anonymize_video(input_path, output_path)
    tasks[uid]["ready"] = True

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    uid = str(uuid.uuid4())

    input_path = f"tmp/{uid}_input.mp4"
    output_path = f"tmp/{uid}_output.mp4"

    with open(input_path, "wb") as f:
        f.write(await file.read())

    tasks[uid] = {
        "ready": False,
        "output": output_path
    }

    thread = threading.Thread(
        target=process_video,
        args=(uid, input_path, output_path)
    )
    thread.start()

    return JSONResponse({"uid": uid})

@app.get("/status/{uid}")
def status(uid: str):
    task = tasks.get(uid)
    if not task:
        return {"ready": False}
    return {"ready": task["ready"]}

@app.get("/download/{uid}")
def download(uid: str):
    task = tasks.get(uid)
    if not task or not task["ready"]:
        return JSONResponse({"error": "Not ready"}, status_code=400)

    return FileResponse(
        task["output"],
        filename="anonymized.mp4",
        media_type="video/mp4"
    )
