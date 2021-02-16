from video_sources.video_base import VideoBase
import os
import mss
import time
import numpy as np
import cv2
import threading


class ScreenCatpure(VideoBase):
    def _start_screen_capture(self):

        with mss.mss() as sct:

            # Part of the screen to capture
            monitor = {"top": 0, "left": 0, "width": self.width, "height": self.height}

            print(monitor)
            while self.vs:

                time.sleep(0.001)
                with self.lock:
                    time.sleep(0.001)

                    img = np.array(sct.grab(monitor))
                    frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

                    self.new_frame = True

                    if self.video_writer:
                        self.video_writer.write(
                            cv2.resize(frame, (monitor["width"], monitor["height"]))
                        )

                    self.output_frame = frame.copy()

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
