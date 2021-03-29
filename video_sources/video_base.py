import os
import sys
import threading
import time
import cv2
from video_sources import get_video_source_name

MAX_VIDEO_STREAMS = 1


class VideoBase(object):
    def __init__(self, camera_index):
        self.vs = None
        self.output_frame = None
        self.lock = threading.Lock()
        self.video_writer = None
        self.new_frame = False
        self.camera_index = camera_index
        self.camera_name = get_video_source_name(camera_index)
        self.height = None
        self.width = None
        self.streaming_index = 0
        self.streaming = {}

    def info(self):

        status = {
            "camera_on": False,
            "camera_record": False,
            "camera_index": self.camera_index,
            "camera_name": self.camera_name,
        }

        with self.lock:
            if self.vs:
                status["camera_on"] = True

                if self.video_writer:
                    status["camera_record"] = True

        return status

    def is_recording(self):
        """ Return True if recording, else False """
        with self.lock:
            if self.video_writer:
                return True

        return False

    def is_on(self):
        """ Return True if camera is on"""

        with self.lock:
            if self.vs:
                return True

        return False

    def _get_new_streaming_index(self):

        with self.lock:
            if len(self.streaming) >= MAX_VIDEO_STREAMS:
                if MAX_VIDEO_STREAMS == 1:
                    for stream_to_end in self.streaming.keys():
                        self.streaming[stream_to_end] = False
                else:
                    for stream_to_end in sorted(self.streaming.keys())[
                        : -(MAX_VIDEO_STREAMS - 1)
                    ]:
                        self.streaming[stream_to_end] = False
            self.streaming_index += 1
            return self.streaming_index - 1

    def generate(self):
        """ Generate an octet stream response consumable by a response stream """

        key = self._get_new_streaming_index()
        self.streaming[key] = True
        print("Stating new video Stream: ", key)
        counter = 0
        while self.streaming.get(key, None):
            if counter % 300 == 0:
                pass
                # print("Report: Video Streaming at ", key)
            counter += 1
            # wait until the lock is acquired
            # start = time.time()
            with self.lock:
                # start_lock = time.time()
                # check if the output frame is available, otherwise skip
                # the iteration of the loop
                if self.output_frame is None or self.new_frame is False:
                    continue
                # encode the frame in JPEG format
                (flag, encoded_image) = cv2.imencode(
                    ".jpg", cv2.resize(self.output_frame, (640, 480))
                )
                # ensure the frame was successfully encoded
                if not flag:
                    continue

                # print("in lock", time.time() - start_lock)
            # yield the output frame in the byte format
            # print("out-lock", time.time() - start)

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + bytearray(encoded_image) + b"\r\n"
            )

        # print("Report: Ending Video Stream ", key)
        del self.streaming[key]

    def record_start(self, filename):

        with self.lock:

            fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Be sure to use the lower case

            # Define the codec and create VideoWriter object
            if not os.path.exists(os.path.dirname(filename)):
                print(
                    "File directory does not exist,  recording to video directory in gateway location."
                )
                if not os.path.exists("./video"):
                    os.mkdir("./video")

                filename = os.path.join("./video", os.path.basename(filename))

            self.video_writer = cv2.VideoWriter(
                filename + ".mp4", fourcc, 24.0, (self.width, self.height)
            )

    def record_stop(self):

        with self.lock:
            if self.video_writer:
                self.video_writer.release()
                self.video_writer = None

    def off(self):
        with self.lock:

            for key in self.streaming.keys():
                self.streaming[key] = False
            self.streaming_index = 0

            if self.video_writer:
                self.video_writer.release()
                self.video_writer = None

            if self.vs:

                try:
                    self.vs.release()
                except Exception as e:
                    print(e)

                time.sleep(1)

                self.vs = None
