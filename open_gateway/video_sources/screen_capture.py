import os
import mss
import time
import numpy as np
import cv2
import threading

from open_gateway.video_sources.video_base import VideoBase

SAMPLES_PER_FRAME = 10.0


class ScreenCatpure(VideoBase):
    @property
    def target_sample_per_frame(self):
        return SAMPLES_PER_FRAME

    @property
    def target_sample_rate(self):
        return 1.0 / self.target_sample_per_frame

    def _start_screen_capture(self):

        with mss.mss() as sct:

            # Part of the screen to capture
            monitor = {"top": 0, "left": 0, "width": self.width, "height": self.height}

            print("Screen Capture Dimensions", monitor)

            frame_counter = 0
            start = frame_time = time.time()
            capture_time = 0

            while self.vs:

                with self.lock:

                    if (time.time() - start) < self.target_sample_rate - capture_time:
                        pass
                    else:
                        start_grab = time.time()
                        img = np.array(sct.grab(monitor))
                        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                        self.new_frame = True
                        self.output_frame = frame.copy()

                        if self.video_writer:
                            self.video_writer.write(
                                cv2.resize(frame, (monitor["width"], monitor["height"]))
                            )

                        start = time.time()
                        capture_time = time.time() - start_grab

                        """
                        print("screen grab took: ", time.time() - start_grab)
                        frame_counter += 1
                        if frame_counter == self.target_sample_per_frame:
                            print(
                                "frames: ", frame_counter, "time:", start - frame_time
                            )
                            frame_time = start
                            frame_counter = 0
                        """

                time.sleep(0.0001)

    def start(self):

        if self.vs is not None:
            return

        print("Starting Screen Capture")
        self.vs = "screen_capture"

        self.width, self.height = set_screen_resolution()

        thread = threading.Thread(target=self._start_screen_capture)
        thread.daemon = True
        thread.start()


def set_screen_resolution():

    from tkinter import Tk

    if os.environ.get("DISPLAY", "") == "":
        print("No Display Found. Using :0.0")
        os.environ.__setitem__("DISPLAY", ":0.0")

    root = Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()

    return width, height


if __name__ == "__main__":
    sc = ScreenCatpure(-1)
    sc.start()
    sc.record_start("test.mp4")

    time.sleep(10)

    sc.record_stop()
    sc.off()
