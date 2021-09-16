import numpy as np
import cv2

cap = cv2.VideoCapture(0)  # Capture video from camera

# Get the width and height of frame
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Be sure to use the lower case
out = cv2.VideoWriter("output.mp4", fourcc, 20.0, (width, height))

while cap.isOpened():
    ret, frame = cap.read()
    if ret == True:
        frame = cv2.flip(frame, 0)

        # write the flipped frame
        out.write(frame)

        cv2.imshow("frame", frame)
        if (cv2.waitKey(1) & 0xFF) == ord("q"):  # Hit `q` to exit
            break
    else:
        break

# Release everything if job is finished
out.release()
cap.release()
cv2.destroyAllWindows()
