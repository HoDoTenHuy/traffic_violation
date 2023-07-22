import os
import cv2
import shutil

from io import BytesIO
from pathlib import Path
from fastapi import UploadFile
from tempfile import NamedTemporaryFile
from utils.constants import COLOR_GREEN


def save_upload_file_tmp(upload_file: UploadFile) -> Path:
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
    finally:
        upload_file.file.close()
    return tmp_path


def delete_tmp_file(path: str):
    if os.path.exists(path):
        os.remove(path)


def convert_pil2bytes(image_pil):
    # Convert the image to bytes
    image_bytes = BytesIO()
    image_pil.save(image_bytes, format="PNG")
    image_bytes.seek(0)
    return image_bytes


def draw_tracking(frame, online_targets):
    # Draw bounding boxes on the frame
    for target in online_targets:
        track_id, class_id, score = target[-3:]
        x1, y1, x2, y2 = map(int, target[:4])

        # Draw the bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Add text with class ID and score
        text = f"{track_id}: {score:.2f}"
        cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_GREEN, 2)
    return frame
