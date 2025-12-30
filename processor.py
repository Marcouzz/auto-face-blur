import cv2
import os
import uuid
import subprocess
from ultralytics import YOLO

MODEL_NAME = "yolov8n.pt"
model = YOLO(MODEL_NAME)

def anonymize_video(input_path, output_path):
    global model

    if not os.path.exists("tmp"):
        os.makedirs("tmp")

    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    temp_video = f"tmp/{uuid.uuid4()}_blur.mp4"

    out = cv2.VideoWriter(
        temp_video,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (W, H)
    )

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame, conf=0.25, iou=0.45, classes=[0], verbose=False)

        if results and results[0].boxes is not None:
            for box in results[0].boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                person_h = y2 - y1
                person_w = x2 - x1

                head_h = int(0.28 * person_h)
                pad_x = int(0.08 * person_w)

                hx1 = max(0, x1 - pad_x)
                hx2 = min(W, x2 + pad_x)
                hy1 = max(0, y1)
                hy2 = min(H, y1 + head_h)

                min_kernel = 15
                max_kernel = 41
                min_sigma = 6
                max_sigma = 20

                ratio = person_h / H
                ratio = min(max(ratio, 0.0), 1.0)

                kernel_size = int(min_kernel + (max_kernel - min_kernel) * ratio)
                if kernel_size % 2 == 0:
                    kernel_size += 1

                sigma = min_sigma + (max_sigma - min_sigma) * ratio

                roi = frame[hy1:hy2, hx1:hx2]
                if roi.size > 0:
                    roi = cv2.GaussianBlur(
                        roi,
                        (kernel_size, kernel_size),
                        sigma
                    )
                    frame[hy1:hy2, hx1:hx2] = roi

        out.write(frame)

    cap.release()
    out.release()

    subprocess.run([
        "ffmpeg", "-y",
        "-i", temp_video,
        "-i", input_path,
        "-map", "0:v:0",
        "-map", "1:a:0?",
        "-map_metadata", "-1",
        "-c:v", "libx264",
        "-c:a", "copy",
        "-preset", "fast",
        "-crf", "23",
        output_path
    ])

    os.remove(temp_video)
