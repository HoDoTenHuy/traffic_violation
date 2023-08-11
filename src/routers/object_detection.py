import io
import logging

from PIL import Image
from fastapi import UploadFile, File
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse, StreamingResponse
from helpers.detector import ObjectDetectionHelper
from utils.config_yaml import ConfigManager
from utils.common import save_upload_file_tmp, delete_tmp_file, convert_pil2bytes

config_manager = ConfigManager()
config = config_manager.get_config()
model_config = config.get('object_config')

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post('/object-detection')
async def object_detection(image: UploadFile = File(...), yolov8_weight: UploadFile = File(...)):
    try:
        weight_path = save_upload_file_tmp(yolov8_weight)
        model_config['weights_path'] = weight_path
        detector = ObjectDetectionHelper(model_config)
        image_path = save_upload_file_tmp(image)
        image = Image.open(image_path)

        outputs = detector.detect(image)

        image_pil = Image.fromarray(outputs[0].plot()[..., ::-1])
        image_bytes = convert_pil2bytes(image_pil)
        delete_tmp_file(str(image_path))
        return StreamingResponse(io.BytesIO(image_bytes.read()), media_type="image/png")
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {e}!"}, status_code=400)
