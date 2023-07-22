import os
import logging

from ultralytics import YOLO
from bytetracker import BYTETracker

logger = logging.getLogger(__name__)

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


class VehicleDetectionHelper:
    def __init__(self, config: dict) -> None:
        self.config = config
        if self.config:
            try:
                self.weights_path = self.config.get('weights_path')
                self.conf_thresh = self.config.get('confidence_score')
                self.iou = self.config.get('non_maxima_suppression_threshold')
                self.input_shape = self.config.get('image_size')
                self.show = self.config.get('show_results')
                self.device = self.config.get('device')
            except KeyError as e:
                logger.critical('event={} message="{}"'.format('load-config-failure',
                                                               'The config file is invalid: {}'.format(e)))
        else:
            logger.critical('event={} message="{}"'.format('load-config-failure', 'The config file is empty.'))

        self.model = self.load_model()

    def load_model(self):
        model = YOLO(self.weights_path)
        return model

    async def detect(self, image):
        outputs = self.model.predict(image, show=self.show, imgsz=self.input_shape,
                                     conf=self.conf_thresh, iou=self.iou, device=self.device)
        return outputs
