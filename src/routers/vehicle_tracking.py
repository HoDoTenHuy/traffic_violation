import io
import logging

from PIL import Image
from pathlib import Path
from fastapi import Header
from fastapi import UploadFile, File
from fastapi.routing import APIRouter
from fastapi import Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, StreamingResponse
from handlers.tracker import VehicleTracker
from helpers.detector import ObjectDetectionHelper
from utils.config_yaml import ConfigManager
from utils.common import save_upload_file_tmp, delete_tmp_file, convert_pil2bytes, draw_line_widget

config_manager = ConfigManager()
config = config_manager.get_config()
model_config = config.get('object_config')

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post('/vehicle-detection')
async def vehicle_detection(image: UploadFile = File(...)):
    try:
        vehicle_detector = ObjectDetectionHelper(model_config)
        tmp_path = save_upload_file_tmp(image)
        image = Image.open(tmp_path)

        outputs = await vehicle_detector.detect(image)

        image_pil = Image.fromarray(outputs[0].plot()[..., ::-1])
        image_bytes = convert_pil2bytes(image_pil)

        delete_tmp_file(str(tmp_path))
        return StreamingResponse(io.BytesIO(image_bytes.read()), media_type="image/png")
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {e}!"}, status_code=400)


@router.post('/vehicle-tracking')
async def vehicle_tracking(video: UploadFile = File(...)):
    try:
        vehicle_tracker = VehicleTracker(model_config)
        tmp_path = save_upload_file_tmp(video)
        # line_widget = draw_line_widget(tmp_path)
        vehicle_tracker.run(str(tmp_path))
        delete_tmp_file(str(tmp_path))
        return JSONResponse(content={"message": "Application is stopping!"}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"message": f"Error: {e}!"}, status_code=400)
