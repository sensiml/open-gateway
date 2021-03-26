from video_sources.video_base import VideoBase
import os
import mss
import time
import numpy as np
import cv2
import threading


SAMPLES_PER_FRAME = 24.0
SAMPLE_RATE = 1.0 / SAMPLES_PER_FRAME - 0.005


class ScreenCatpure(VideoBase):
    def _start_screen_capture(self):

        with mss.mss() as sct:

            # Part of the screen to capture
            monitor = {"top": 0, "left": 0, "width": self.width, "height": self.height}

            print("Screen Capture Dimensions", monitor)

            frame_counter = 0
            start = time.time()
            frame_time = start
            tracker = start

            while self.vs:

                with self.lock:
                    if (time.time() - start) < SAMPLE_RATE:
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

                        """
                        print("screen garb took: ", time.time() - start_grab)

                        frame_counter += 1
                        tmp = time.time()
                        print((tmp - tracker))
                        tracker = tmp
                        if frame_counter == SAMPLES_PER_FRAME:
                            print(
                                "frames: ", frame_counter, "time:", tracker - frame_time
                            )
                            frame_time = tracker
                            frame_counter = 0
                        """

                time.sleep(0.0001)

    def start(self):

        if self.vs is not None:
            return

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
