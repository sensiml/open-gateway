import serial.tools.list_ports
import json
import struct
import math
import time
import random
from sources.base import BaseReader

SHORT = 2
INT16_BYTE_SIZE = 2


class TestReader(BaseReader):
    """ Base Reader Object, describes the methods that must be implemented for each data source"""

    def __init__(self, config, device_id=None, **kwargs):

        super(TestReader, self).__init__(config, **kwargs)

    @property
    def delay(self):
        return 1.0 / self.sample_rate * self.samples_per_packet / 1.25

    @property
    def byteSize(self):
        if self.config_columns:
            return self.samples_per_packet * len(self.config_columns) * INT16_BYTE_SIZE

        return 0

    def _generate_samples(self, num_columns, sample_rate):
        fs = sample_rate * 10
        f = sample_rate

        x = list(range(0, fs))  # the points on the x axis for plotting

        return [
            [
                1000 * offset
                + 1000 * math.sin(2 * math.pi * f * (float(xs * offset * 3.14) / fs))
                for xs in x
            ]
            for offset in range(num_columns)
        ]

    def _pack_data(self, data, byteSize, samples_per_packet, start_index):
        sample_data = bytearray(byteSize)
        num_cols = len(data)
        data_len = len(data[0])
        end_index = start_index + samples_per_packet
        if end_index > data_len:
            end_index -= data_len

        for x in range(0, samples_per_packet):
            if x + start_index >= data_len:
                start_index = 0
            for y in range(0, num_cols):
                struct.pack_into(
                    "<h",
                    sample_data,
                    (y + (x * num_cols)) * 2,
                    random.randint(-50, 50) + int(data[y][x + start_index]),
                )

        return bytes(sample_data), end_index

    def list_available_devices(self):
        return [{"id": 1, "name": "Test Data", "device_id": "Tester"}]

    def get_device_info(self):
        pass

    def set_config(self, config):

        config["CONFIG_COLUMNS"] = {
            "AccelerometerX": 0,
            "AccelerometerY": 1,
            "AccelerometerZ": 2,
            "GyroscopeX": 3,
            "GyroscopeY": 4,
            "GyroscopeZ": 5,
        }
        config["CONFIG_SAMPLE_RATE"] = 119
        config["DATA_SOURCE"] = "TEST"

        self.samples_per_packet = config["CONFIG_SAMPLES_PER_PACKET"]
        self.sample_rate = config["CONFIG_SAMPLE_RATE"]
        self.config_columns = config.get("CONFIG_COLUMNS")

    def send_connect(self):
        pass

    def read_data(self):
        index = 0
        data = self._generate_samples(len(self.config_columns), self.sample_rate)
        self.streaming = True
        while self.streaming:
            sample_data, index = self._pack_data(
                data, self.byteSize, self.samples_per_packet, index
            )
            yield sample_data
            time.sleep(self.delay)


class TestResultReader(BaseReader):
    def __init__(self, config, device_id=None, connect=True, **kwargs):

        self.streaming = False

        super(TestResultReader, self).__init__(config, **kwargs)

    def set_config(self, config):
        config["DATA_SOURCE"] = "TEST"

    def read_data(self):

        self.streaming = True
        counter = 0
        while self.streaming:
            time.sleep(1)

            yield json.dumps(
                self._map_classification(
                    {"ModelNumber": 0, "Classification": random.randint(0, 10)}
                )
            ) + "\n"
            counter += 1
