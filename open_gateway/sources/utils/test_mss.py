import os
import mss
import time
import numpy as np
import cv2
import threading


SAMPLES_PER_FRAME = 24.0
SAMPLE_RATE = 1.0 / SAMPLES_PER_FRAME - 0.005


from tkinter import Tk

if os.environ.get("DISPLAY", "") == "":
    print("No Display Found. Using :0.0")
    os.environ.__setitem__("DISPLAY", ":0.0")

root = Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.destroy()


# Part of the screen to capture
monitor = {"top": 0, "left": 0, "width": width, "height": height}

print("Screen Capture Dimensions", monitor)

for i in range(10000):
    with mss.mss() as sct:

        frame_counter = 0
        start = time.time()
        frame_time = start
        tracker = start

        start_grab = time.time()
        img = np.array(sct.grab(monitor))
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        start = time.time()

        # """
        print("screen garb took: ", time.time() - start_grab)

        frame_counter += 1
        tmp = time.time()
        print((tmp - tracker))
        tracker = tmp
        if frame_counter == SAMPLES_PER_FRAME:
            print("frames: ", frame_counter, "time:", tracker - frame_time)
            frame_time = tracker
            frame_counter = 0
        # """

        time.sleep(0.0001)
