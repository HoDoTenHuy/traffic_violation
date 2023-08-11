import logging

from fastapi.routing import APIRouter
from fastapi.responses import StreamingResponse
from utils.config_yaml import ConfigManager
from handlers.streaming import Streaming

router = APIRouter(prefix='/streaming')

config_manager = ConfigManager()
config = config_manager.get_config()
streaming_config = config.get('streaming')

logger = logging.getLogger(__name__)


@router.get('/video')
async def generate_video() -> StreamingResponse:
    streaming = Streaming(streaming_config)
    return StreamingResponse(streaming.generate_frame_streaming(),
                             media_type="multipart/x-mixed-replace;boundary=frame")

