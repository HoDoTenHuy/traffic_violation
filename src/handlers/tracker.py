import cv2
import logging

from utils.VideoPlayer import VideoPlayer
from helpers.detector import VehicleDetectionHelper

logger = logging.getLogger(__name__)


class VehicleTracker:
    def __init__(self, config):
        self.frame_id = 0
        self.violators_count = 0
        self.vehicle_count = 0
        self.config = config
        self.vehicle_detection_helper = VehicleDetectionHelper(self.config)
        if self.config:
            try:
                self.conf_thresh = self.config.get('Detection').get('confidence_score')
                self.nms_thresh = self.config.get('Detection').get('non_maxima_suppression_threshold')
                self.skip_frame = self.config.get('Setting').get('skip_frame')
                self.video_output = self.config.get('Video').get('video_output')
            except KeyError as e:
                logger.critical('event={} message="{}"'.format('load-config-failure',
                                                               'The config file is invalid: {}'.format(e)))
            else:
                logger.critical('event={} message="{}"'.format('load-config-failure', 'The config file is empty.'))

    async def run(self, file_path: str):
        await self.tear_down()
        camera_player = VideoPlayer(file_path)
        if camera_player.video_cap is None:
            logger.error('event={} message="{}"'.format('load-video-failure', 'The video not found!'))
            exit(-1)

        video_writer = await self.__init_writer(fps=camera_player.fps, w=camera_player.width, h=camera_player.height)

    async def __init_writer(self, fps, w, h):
        video_writer = cv2.VideoWriter(self.video_output, cv2.VideoWriter_fourcc(*'FMP4'), fps, (w, h))
        return video_writer

    async def tear_down(self):
        self.frame_id = 0
        self.violators_count = 0
        self.vehicle_count = 0
