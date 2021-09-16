import sys
import os
import subprocess
import re
import threading
import time
import cv2

from open_gateway.video_sources.video_base import VideoBase

SAMPLES_PER_FRAME = 24.0


class WebCam(VideoBase):
    @property
    def target_sample_per_frame(self):
        return SAMPLES_PER_FRAME

    @property
    def target_sample_rate(self):
        return 1.0 / self.target_sample_per_frame

    def _start_webcam(self):

        start = time.time()
        capture_time = 0
        frame_time = start
        frame_counter = 0

        while self.vs.isOpened():
            with self.lock:
                if self.vs is None:
                    return

                if (time.time() - start) < self.target_sample_rate - capture_time * 1.2:
                    pass
                else:
                    start_grab = time.time()

                    self.new_frame, frame = self.vs.read()

                    if self.new_frame:
                        if self.video_writer:
                            self.video_writer.write(frame)

                        self.output_frame = frame.copy()

                    start = time.time()
                    capture_time = start - start_grab

                    """
                    frame_counter += 1
                    # print("camera capture took: ", time.time() - start_grab)
                    if frame_counter == self.target_sample_per_frame:
                        print("frames: ", frame_counter, "time:", start - frame_time)
                        frame_time = start
                        frame_counter = 0
                    """

            time.sleep(0.0001)

    def start(self):

        if self.vs is not None:
            return

        print("Starting Camera: ", self.camera_index)
        self.vs = cv2.VideoCapture(self.camera_index)

        self.width = int(self.vs.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
        self.height = int(self.vs.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)

        # start a thread that will perform motion detection
        thread = threading.Thread(target=self._start_webcam)
        thread.daemon = True
        thread.start()


if __name__ == "__main__":
    wc = WebCam(0)
    wc.start()
    wc.record_start("test.mp4")

    time.sleep(10)

    wc.record_stop()
    wc.off()
