import sys
import os
import subprocess
import re
import threading
import time
import cv2

from video_sources.video_base import VideoBase

SAMPLES_PER_FRAME = 24.0
SAMPLE_RATE = 1.0 / SAMPLES_PER_FRAME - 0.003


class WebCam(VideoBase):
    def _start_webcam(self):

        frame_counter = 0
        start = time.time()
        frame_time = start
        tracker = start

        while self.vs.isOpened():
            with self.lock:
                if self.vs is None:
                    return

                if (time.time() - start) < SAMPLE_RATE:
                    pass
                else:

                    self.new_frame, frame = self.vs.read()

                    if self.new_frame:
                        if self.video_writer:
                            self.video_writer.write(frame)

                        self.output_frame = frame.copy()

                    start = time.time()

                    """
                    frame_counter += 1
                    tmp = time.time()
                    # print((tmp - tracker))
                    tracker = tmp
                    if frame_counter == SAMPLES_PER_FRAME:
                        print("frames: ", frame_counter, "time:", tracker - frame_time)
                        frame_time = tracker
                        frame_counter = 0
                    """

            time.sleep(0.0001)

    def start(self):

        if self.vs is not None:
            return

        print("Starting Camera")
        print(self.camera_index)
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
