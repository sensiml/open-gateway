import sys
import os
import subprocess
import re
import threading
import time
import cv2

from video_sources.video_base import VideoBase


class WebCam(VideoBase):
    def _start_webcam(self):

        while self.vs.isOpened():
            start = time.time()
            time.sleep(0.001)
            with self.lock:
                time.sleep(0.001)
                start_lock = time.time()

                if self.vs is None:
                    return

                self.new_frame, frame = self.vs.read()

                if self.new_frame:
                    if self.video_writer:
                        self.video_writer.write(frame)

                    self.output_frame = frame.copy()
                # print("webcam in-lock", self.new_frame, time.time() - start_lock)
            # print("webcam out-lock", time.time() - start)

    def start(self):

        if self.vs is not None:
            return

        print("starting")
        print(self.camera_index)
        self.vs = cv2.VideoCapture(self.camera_index)
        time.sleep(2)
        print("here")

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
