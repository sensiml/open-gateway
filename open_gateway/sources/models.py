import json
import struct
import math
import time
import random

from open_gateway.sources.base import (
    BaseReader,
    BaseResultReaderMixin,
    BaseStreamReaderMixin,
)
from open_gateway.video_sources.webcam import MediapipeHandWebCam

class ModelReader(BaseReader):
    name = "MODEL"

    def list_available_devices(self):
        return [
            {"id": 1, "name": "Mediapipe Hand Tracking", "device_id": "Mediapipe Hand Tracking"},
        ]


class HandModelStreamReader(ModelReader, BaseStreamReaderMixin):
    
    def has_video_source(self):
        return True
    
    def get_video_source(self):
        return self.video_source

    @property
    def byteSize(self):
        if self.config_columns:
            return (
                self.source_samples_per_packet
                * len(self.config_columns)
                * self.data_byte_size
            )

        return 0

    def _generate_samples(self, num_columns, sample_rate):
        fs = sample_rate

        x = list(range(0, fs))  # the points on the x axis for plotting

        data = [[10 * offset + xs for xs in x] for offset in range(0, num_columns)]

        sample_data = bytearray(num_columns * len(x) * self.data_byte_size)

        for index in x:
            for y in range(0, num_columns):
                struct.pack_into(
                    "<" + self.data_type_str,
                    sample_data,
                    (y + (index * num_columns)) * self.data_byte_size,
                    self.data_type_cast(float(data[y][index]) + 0.5),
                )

        return bytes(sample_data), len(x)


    def read_device_config(self):

        config = get_test_device_configs(self.device_id)

        self._validate_config(config)

        return config
    
    def _read_source(self):

        self.streaming = True
        self.video_source = MediapipeHandWebCam(0)
        self.video_source.set_data_buffer(self.buffer)
        self.video_source.start()
        

        while self.streaming:
            time.sleep(0.0001)
            continue
                        




def get_test_device_configs(device_id):

    config = {}

    if device_id == "Mediapipe Hand Tracking":
        config["column_location"] = {'L_WRIST_X': 0,
 'L_WRIST_Y': 1,
 'L_WRIST_Z': 2,
 'L_THUMB_CMC_X': 3,
 'L_THUMB_CMC_Y': 4,
 'L_THUMB_CMC_Z': 5,
 'L_THUMB_MCP_X': 6,
 'L_THUMB_MCP_Y': 7,
 'L_THUMB_MCP_Z': 8,
 'L_THUMB_IP_X': 9,
 'L_THUMB_IP_Y': 10,
 'L_THUMB_IP_Z': 11,
 'L_THUMB_TIP_X': 12,
 'L_THUMB_TIP_Y': 13,
 'L_THUMB_TIP_Z': 14,
 'L_INDEX_FINGER_MCP_X': 15,
 'L_INDEX_FINGER_MCP_Y': 16,
 'L_INDEX_FINGER_MCP_Z': 17,
 'L_INDEX_FINGER_PIP_X': 18,
 'L_INDEX_FINGER_PIP_Y': 19,
 'L_INDEX_FINGER_PIP_Z': 20,
 'L_INDEX_FINGER_DIP_X': 21,
 'L_INDEX_FINGER_DIP_Y': 22,
 'L_INDEX_FINGER_DIP_Z': 23,
 'L_INDEX_FINGER_TIP_X': 24,
 'L_INDEX_FINGER_TIP_Y': 25,
 'L_INDEX_FINGER_TIP_Z': 26,
 'L_MIDDLE_FINGER_MCP_X': 27,
 'L_MIDDLE_FINGER_MCP_Y': 28,
 'L_MIDDLE_FINGER_MCP_Z': 29,
 'L_MIDDLE_FINGER_PIP_X': 30,
 'L_MIDDLE_FINGER_PIP_Y': 31,
 'L_MIDDLE_FINGER_PIP_Z': 32,
 'L_MIDDLE_FINGER_DIP_X': 33,
 'L_MIDDLE_FINGER_DIP_Y': 34,
 'L_MIDDLE_FINGER_DIP_Z': 35,
 'L_MIDDLE_FINGER_TIP_X': 36,
 'L_MIDDLE_FINGER_TIP_Y': 37,
 'L_MIDDLE_FINGER_TIP_Z': 38,
 'L_RING_FINGER_MCP_X': 39,
 'L_RING_FINGER_MCP_Y': 40,
 'L_RING_FINGER_MCP_Z': 41,
 'L_RING_FINGER_PIP_X': 42,
 'L_RING_FINGER_PIP_Y': 43,
 'L_RING_FINGER_PIP_Z': 44,
 'L_RING_FINGER_DIP_X': 45,
 'L_RING_FINGER_DIP_Y': 46,
 'L_RING_FINGER_DIP_Z': 47,
 'L_RING_FINGER_TIP_X': 48,
 'L_RING_FINGER_TIP_Y': 49,
 'L_RING_FINGER_TIP_Z': 50,
 'L_PINKY_MCP_X': 51,
 'L_PINKY_MCP_Y': 52,
 'L_PINKY_MCP_Z': 53,
 'L_PINKY_PIP_X': 54,
 'L_PINKY_PIP_Y': 55,
 'L_PINKY_PIP_Z': 56,
 'L_PINKY_DIP_X': 57,
 'L_PINKY_DIP_Y': 58,
 'L_PINKY_DIP_Z': 59,
 'L_PINKY_TIP_X': 60,
 'L_PINKY_TIP_Y': 61,
 'L_PINKY_TIP_Z': 62,
 'R_WRIST_X': 63,
 'R_WRIST_Y': 64,
 'R_WRIST_Z': 65,
 'R_THUMB_CMC_X': 66,
 'R_THUMB_CMC_Y': 67,
 'R_THUMB_CMC_Z': 68,
 'R_THUMB_MCP_X': 69,
 'R_THUMB_MCP_Y': 70,
 'R_THUMB_MCP_Z': 71,
 'R_THUMB_IP_X': 72,
 'R_THUMB_IP_Y': 73,
 'R_THUMB_IP_Z': 74,
 'R_THUMB_TIP_X': 75,
 'R_THUMB_TIP_Y': 76,
 'R_THUMB_TIP_Z': 77,
 'R_INDEX_FINGER_MCP_X': 78,
 'R_INDEX_FINGER_MCP_Y': 79,
 'R_INDEX_FINGER_MCP_Z': 80,
 'R_INDEX_FINGER_PIP_X': 81,
 'R_INDEX_FINGER_PIP_Y': 82,
 'R_INDEX_FINGER_PIP_Z': 83,
 'R_INDEX_FINGER_DIP_X': 84,
 'R_INDEX_FINGER_DIP_Y': 85,
 'R_INDEX_FINGER_DIP_Z': 86,
 'R_INDEX_FINGER_TIP_X': 87,
 'R_INDEX_FINGER_TIP_Y': 88,
 'R_INDEX_FINGER_TIP_Z': 89,
 'R_MIDDLE_FINGER_MCP_X': 90,
 'R_MIDDLE_FINGER_MCP_Y': 91,
 'R_MIDDLE_FINGER_MCP_Z': 92,
 'R_MIDDLE_FINGER_PIP_X': 93,
 'R_MIDDLE_FINGER_PIP_Y': 94,
 'R_MIDDLE_FINGER_PIP_Z': 95,
 'R_MIDDLE_FINGER_DIP_X': 96,
 'R_MIDDLE_FINGER_DIP_Y': 97,
 'R_MIDDLE_FINGER_DIP_Z': 98,
 'R_MIDDLE_FINGER_TIP_X': 99,
 'R_MIDDLE_FINGER_TIP_Y': 100,
 'R_MIDDLE_FINGER_TIP_Z': 101,
 'R_RING_FINGER_MCP_X': 102,
 'R_RING_FINGER_MCP_Y': 103,
 'R_RING_FINGER_MCP_Z': 104,
 'R_RING_FINGER_PIP_X': 105,
 'R_RING_FINGER_PIP_Y': 106,
 'R_RING_FINGER_PIP_Z': 107,
 'R_RING_FINGER_DIP_X': 108,
 'R_RING_FINGER_DIP_Y': 109,
 'R_RING_FINGER_DIP_Z': 110,
 'R_RING_FINGER_TIP_X': 111,
 'R_RING_FINGER_TIP_Y': 112,
 'R_RING_FINGER_TIP_Z': 113,
 'R_PINKY_MCP_X': 114,
 'R_PINKY_MCP_Y': 115,
 'R_PINKY_MCP_Z': 116,
 'R_PINKY_PIP_X': 117,
 'R_PINKY_PIP_Y': 118,
 'R_PINKY_PIP_Z': 119,
 'R_PINKY_DIP_X': 120,
 'R_PINKY_DIP_Y': 121,
 'R_PINKY_DIP_Z': 122,
 'R_PINKY_TIP_X': 123,
 'R_PINKY_TIP_Y': 124,
 'R_PINKY_TIP_Z': 125}
        
        config["sample_rate"] = 24
        config["samples_per_packet"] = 4
        config["data_type"] = "int"

  

    else:
        raise Exception("Invalid Device ID")

    return config

