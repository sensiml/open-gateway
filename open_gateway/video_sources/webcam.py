import sys
import os
import subprocess
import re
import threading
import struct
import time
import cv2
try:
    import mediapipe as mp
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose
except:
    print("Mediapipe not installed")
    pass

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
                            self.video_writer.write(cv2.flip(frame, 1))

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



class MediapipeHandWebCam(WebCam):
    
    data_byte_size = 2
    data_type_str = 'h'
    data_type_cast = int
    
    def set_data_buffer(self, data_buffer):
        self.data_buffer=data_buffer

    def _start_webcam(self):

        start = time.time()
        capture_time = 0
        frame_time = start
        frame_counter = 0

        with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
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
                
                            frame.flags.writeable = False
                            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            results = hands.process(frame)
                            frame.flags.writeable = True
                            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                            keypoints = bytearray(42 * 3 * self.data_byte_size)
                            if results.multi_hand_landmarks:   
                                for index, hand_landmarks in enumerate(results.multi_hand_landmarks):                                   
                                    for hand_landmark_index, data_point in enumerate(hand_landmarks.landmark):                                    
                                        struct.pack_into(
                                            "<" + self.data_type_str,
                                            keypoints,
                                            (0 + (index * 21)+(hand_landmark_index*3)) * self.data_byte_size,
                                                self.data_type_cast((float(data_point.x)*10000)),
                                        )
                                        struct.pack_into(
                                                "<" + self.data_type_str,
                                                keypoints,
                                                (1 + (index * 21)+(hand_landmark_index*3)) * self.data_byte_size,
                                                 self.data_type_cast((float(data_point.y)*10000)),
                                            )
                                        struct.pack_into(
                                                "<" + self.data_type_str,
                                                keypoints,
                                                (2 + (index * 21)+(hand_landmark_index*3)) * self.data_byte_size,
                                                 self.data_type_cast((float(data_point.z)*10000)),
                                            )

                                    
                                    mp_drawing.draw_landmarks(
                                        frame,
                                        hand_landmarks,
                                        mp_hands.HAND_CONNECTIONS,
                                        mp_drawing_styles.get_default_hand_landmarks_style(),
                                        mp_drawing_styles.get_default_hand_connections_style())
                            if self.video_writer:
                                self.video_writer.write(cv2.flip(frame, 1))
                            
                            
                            self.data_buffer.update_buffer(keypoints)

                            self.output_frame = frame.copy()

                        start = time.time()
                        capture_time = start - start_grab

                time.sleep(0.0001)



class MediapipePoseWebCam(WebCam):
    
    data_byte_size = 2
    data_type_str = 'h'
    data_type_cast = int
    
    def set_data_buffer(self, data_buffer):
        self.data_buffer=data_buffer

    def _start_webcam(self):

        start = time.time()
        capture_time = 0
        frame_time = start
        frame_counter = 0

        with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:
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
                
                            frame.flags.writeable = False
                            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            results = pose.process(frame)
                            frame.flags.writeable = True
                            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                            keypoints = bytearray(33  * 3 * self.data_byte_size)


                            if results.pose_landmarks:                   
                                for landmark_index, data_point in enumerate(results.pose_landmarks.landmark):                                    
                                    struct.pack_into(
                                        "<" + self.data_type_str,
                                        keypoints,
                                        (0 +(landmark_index*3)) * self.data_byte_size,
                                            self.data_type_cast((float(data_point.x)*1000)),
                                    )
                                    struct.pack_into(
                                            "<" + self.data_type_str,
                                            keypoints,
                                            (1 +(landmark_index*3)) * self.data_byte_size,
                                                self.data_type_cast((float(data_point.y)*1000)),
                                        )
                                    struct.pack_into(
                                            "<" + self.data_type_str,
                                            keypoints,
                                            (2 + (landmark_index*3)) * self.data_byte_size,
                                                self.data_type_cast((float(data_point.z)*1000)),
                                        )

                                
                            mp_drawing.draw_landmarks(
                                    frame,
                                    results.pose_landmarks,
                                    mp_pose.POSE_CONNECTIONS,
                                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
                            if self.video_writer:
                                self.video_writer.write(cv2.flip(frame, 1))
                            
                            
                            self.data_buffer.update_buffer(keypoints)

                            self.output_frame = frame.copy()

                        start = time.time()
                        capture_time = start - start_grab

                time.sleep(0.0001)


if __name__ == "__main__":
    wc = WebCam(0)
    wc.start()
    wc.record_start("test.mp4")

    time.sleep(10)

    wc.record_stop()
    wc.off()


