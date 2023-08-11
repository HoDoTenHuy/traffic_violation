import time
import logging
import threading
import numpy as np

from abc import abstractmethod
from typing import Dict, Optional, Iterator
from handlers.sreaming_event import StreamingEvent

logger = logging.getLogger(__name__)


class BaseStreaming:
    def __init__(self, args, *kwargs) -> None:
        """Start the background camera thread if it isn't running yet."""
        self.image_encode_extension = 'jpeg'
        self.frame: Optional[bytes] = None  # current frame is stored here by background thread
        self.thread: Optional[threading.Thread] = None  # background thread that reads frames from camera
        self.event = StreamingEvent(timeout=10)
        self.start_thread()

    def get_frame(self) -> np.array:
        """Return the current camera frame."""
        # wait for a signal from the camera thread
        self.event.wait()
        self.event.clear()
        return self.frame

    def start_thread(self) -> None:
        # start background frame thread
        self.thread = threading.Thread(target=self._thread, name="Thread Camera ID {}".format('222222'))
        self.thread.start()
        pass

    @abstractmethod
    def run(self):
        pass

    def _thread(self) -> None:
        """Camera background thread."""
        logger.info('event=start-thread message="Starting number pigs thread."')
        info_iterator = self.run()
        for frame in info_iterator:
            self.frame = frame
            self.event.set()  # send signal to clients
            time.sleep(0)

    def generate_frame_streaming(self) -> Iterator[bytes]:
        """Video streaming generator function."""
        while True:
            frame = self.get_frame()
            if self.image_encode_extension == 'jpeg':
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + bytearray(frame) + b'\r\n')
            elif self.image_encode_extension == 'png':
                yield (b'--frame\r\n'
                       b'Content-Type: image/png\r\n\r\n' + bytearray(frame) + b'\r\n')
            else:
                break
