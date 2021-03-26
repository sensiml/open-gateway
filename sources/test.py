import json
import struct
import math
import time
import random

try:
    from sources.base import BaseReader, BaseResultReaderMixin, BaseStreamReaderMixin
except:
    from base import BaseReader, BaseResultReaderMixin, BaseStreamReaderMixin

SHORT = 2
INT16_BYTE_SIZE = 2


class TestReader(BaseReader):
    @property
    def delay(self):
        return 1.0 / self.sample_rate * self.samples_per_packet / 1.25

    @property
    def byteSize(self):
        if self.config_columns:
            return (
                self.source_samples_per_packet
                * len(self.config_columns)
                * INT16_BYTE_SIZE
            )

        return 0

    def _generate_samples(self, num_columns, sample_rate):
        fs = sample_rate

        x = list(range(0, fs))  # the points on the x axis for plotting

        data = [
            [1000 * offset + xs - 32767 for xs in x] for offset in range(0, num_columns)
        ]

        sample_data = bytearray(num_columns * len(x) * 2)
        for index in x:
            for y in range(0, num_columns):
                struct.pack_into(
                    "<h",
                    sample_data,
                    (y + (index * num_columns)) * 2,
                    int(data[y][index]),
                )

        return bytes(sample_data), len(x)

    def _pack_data(self, data, data_len, num_columns, samples_per_packet, start_index):

        start = start_index * 2 * num_columns

        if samples_per_packet + start_index > data_len:
            end_index = data_len - (start_index + samples_per_packet)
            end = end_index * 2 * num_columns

            return data[start:] + data[:end], end_index

        else:
            end_index = start_index + samples_per_packet
            end = end_index * 2 * num_columns
            return data[start:end], end_index

    def list_available_devices(self):
        return [
            {"id": 1, "name": "Test Data", "device_id": "Test IMU 6-axis"},
            {"id": 2, "name": "Test Data", "device_id": "Test Audio"},
        ]


class TestStreamReader(TestReader, BaseStreamReaderMixin):
    def read_device_config(self):

        config = get_test_device_configs(self.device_id)

        self._validate_config(config)

        return config

    def set_app_config(self, config):

        config["DATA_SOURCE"] = "TEST"
        config["CONFIG_COLUMNS"] = self.config_columns
        config["CONFIG_SAMPLE_RATE"] = self.sample_rate
        config["SOURCE_SAMPLES_PER_PACKET"] = self.source_samples_per_packet
        config["DEVICE_ID"] = self.device_id

    def _read_source(self):
        print("Starting to read source test")
        index = 0

        data, data_len = self._generate_samples(
            len(self.config_columns), self.sample_rate
        )

        self.streaming = True

        sleep_time = self.source_samples_per_packet / float(self.sample_rate)
        while self.streaming:
            incycle = time.time()

            try:
                sample_data, index = self._pack_data(
                    data,
                    data_len,
                    self.data_width,
                    self.source_samples_per_packet,
                    index,
                )

                self.buffer.update_buffer(sample_data)

            except Exception as e:
                self.disconnect()
                raise e

            incycle = time.time() - incycle

            time.sleep(sleep_time - incycle)


class TestResultReader(BaseReader, BaseResultReaderMixin):
    def set_app_config(self, config):
        config["DATA_SOURCE"] = "TEST"
        config["DEVICE_ID"] = self.device_id

    def _read_source(self):

        self.streaming = True

        while self.streaming:

            self.rbuffer.update_buffer(
                [
                    json.dumps(
                        self._map_classification(
                            {"ModelNumber": 0, "Classification": random.randint(0, 10)}
                        )
                    )
                ]
            )
            time.sleep(2)


def get_test_device_configs(device_id):

    config = {}
    if device_id == "Test IMU 6-axis":
        config["column_location"] = {
            "AccelerometerX": 0,
            "AccelerometerY": 1,
            "AccelerometerZ": 2,
            "GyroscopeX": 3,
            "GyroscopeY": 4,
            "GyroscopeZ": 5,
        }
        config["sample_rate"] = 104
        config["samples_per_packet"] = 6

    elif device_id == "Test Audio":
        config["column_location"] = {"Microphone": 0}
        config["sample_rate"] = 16000
        config["samples_per_packet"] = 480

    else:
        raise Exception("Invalid Device ID")

    return config


if __name__ == "__main__":
    config = {
        "CONFIG_SAMPLES_PER_PACKET": 10,
        "CONFIG_SAMPLE_RATE": 100,
        "CONFIG_COLUMNS": ["X", "Y", "Z"],
    }
    t = TestReader(config, "Test IMU 6-axis")

    t.set_config(config)

    t.connect()

    t.record_start("tester")

    time.sleep(5)

    t.record_stop()

    t.disconnect()
