import cv2
import time
import logging

from bytetracker import BYTETracker
from utils.common import draw_tracking
from typing import Generator, Optional
from exceptiongroup._formatting import _
from utils.VideoPlayer import VideoPlayer
from utils.config_yaml import ConfigManager
from handlers.base_streaming import BaseStreaming
from helpers.detector import ObjectDetectionHelper
from utils.constants import POSITION_FPS, THICKNESS, COLOR_RED

config_manager = ConfigManager()
config = config_manager.get_config()
model_config = config.get('object_config')

logger = logging.getLogger(__name__)

vehicle_detection_helper = ObjectDetectionHelper(model_config)


class Streaming(BaseStreaming):
    frame_id: int = 0

    def __init__(self, args, *kwargs) -> None:
        super().__init__(args, *kwargs)
        self.file_path = 'models/222222222.mp4'
        self.skip_frame = 1

    def run(self) -> Optional[Generator]:
        camera_player = VideoPlayer('models/222222222.mp4')
        if camera_player.video_cap is None:
            logger.error('event={} message="{}"'.format('load-video-failure', 'The video not found!'))
            exit(-1)

        tracker = BYTETracker()

        try:
            while True:
                grabbed, frame = camera_player.get_frame()

                if not grabbed:
                    break

                if self.frame_id % self.skip_frame == 0:
                    st = time.time()
                    outputs = vehicle_detection_helper.detect(frame)
                    dets = outputs[0]
                    dets = dets.boxes.data.cpu()
                    online_targets = tracker.update(dets, _)

                    frame = draw_tracking(frame, online_targets)

                    cv2.putText(frame, 'FPS: %0.2f' % (1.0 / (time.time() - st)), POSITION_FPS,
                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, COLOR_RED, thickness=THICKNESS,
                                lineType=cv2.LINE_4)

                    (flag, frame_show) = cv2.imencode(f'.{self.image_encode_extension}', frame)
                    if not flag:
                        continue
                    yield frame_show
        except:
            print("User Disconnected")
