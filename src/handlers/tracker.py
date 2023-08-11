import os
import cv2
import time
import logging

from bytetracker import BYTETracker
from utils.common import draw_tracking
from exceptiongroup._formatting import _
from utils.VideoPlayer import VideoPlayer
from helpers.detector import ObjectDetectionHelper
from utils.constants import POSITION_FPS, THICKNESS, COLOR_RED


logger = logging.getLogger(__name__)

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


class VehicleTracker:
    def __init__(self, config):
        self.frame_id = 0
        self.violators_count = 0
        self.vehicle_count = 0
        self.start_time = 0
        self.config = config
        self.vehicle_detection_helper = ObjectDetectionHelper(self.config)
        if self.config:
            try:
                self.conf_thresh = self.config.get('confidence_score')
                self.nms_thresh = self.config.get('non_maxima_suppression_threshold')
                self.skip_frame = self.config.get('skip_frame')
                self.video_output = self.config.get('video_output')
            except KeyError as e:
                logger.critical('event={} message="{}"'.format('load-config-failure',
                                                               'The config file is invalid: {}'.format(e)))
            else:
                logger.critical('event={} message="{}"'.format('load-config-failure', 'The config file is empty.'))

    def run(self, file_path: str):
        self.tear_down()
        camera_player = VideoPlayer(file_path)
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
                    self.start_time = time.time()
                    outputs = self.vehicle_detection_helper.detect(frame)
                    dets = outputs[0]
                    dets = dets.boxes.data.cpu()
                    online_targets = tracker.update(dets, _)

                    frame = draw_tracking(frame, online_targets)

                    cv2.putText(frame, 'FPS: %0.2f' % (1.0 / (time.time() - self.start_time)), POSITION_FPS,
                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, COLOR_RED, thickness=THICKNESS, lineType=cv2.LINE_4)
                    cv2.imshow('frame', frame)

                    yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
        except:
            print("User Disconnected")

        '''
            cv_key = cv2.waitKey(1)
            if cv_key is ord('q'):
                break
        cv2.destroyAllWindows()
        '''

    def tear_down(self):
        self.frame_id = 0
        self.violators_count = 0
        self.vehicle_count = 0
