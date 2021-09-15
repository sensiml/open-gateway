import numpy as np
import cv2
import threading
import time

lock = threading.Lock()
cap = cv2.VideoCapture(0)  # Capture video from camera
output_frame = None
ret = False


def start_webcam():
    global cap, ret, lock, output_frame

    while cap.isOpened():

        start = time.time()
        with lock:
            start_in_lock = time.time()
            ret, frame = cap.read()
            if ret:

                output_frame = frame.copy()
                print("lock", time.time() - start_in_lock)

        now = time.time()
        print("lock start out", now - start_in_lock)
        print("out lock", now - start)


# start a thread that will perform motion detection

thread = threading.Thread(target=start_webcam)
thread.daemon = True
thread.start()


while cap.isOpened():
    with lock:
        if ret == True:
            cv2.imshow("frame", output_frame)
            if (cv2.waitKey(1) & 0xFF) == ord("q"):  # Hit `q` to exit
                break
        else:
            break

# Release everything if job is finished
out.release()
cap.release()
cv2.destroyAllWindows()
