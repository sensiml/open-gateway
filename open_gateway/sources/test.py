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


class TestReader(BaseReader):
    name = "TEST"

    def list_available_devices(self):
        return [
            {"id": 1, "name": "Test IMU 6-axis", "device_id": "Test IMU 6-axis"},
            {"id": 2, "name": "Test Audio", "device_id": "Test Audio"},
            {
                "id": 3,
                "name": "Test IMU 6-axis Float",
                "device_id": "Test IMU 6-axis Float",
            },
            {"id": 4, "name": "Test Acc", "device_id": "Test IMU 3-axis"},
            {"id": 5, "name": " Test IMU 9-axis", "device_id": "Test IMU 9-axis float"},
        ]


class TestStreamReader(TestReader, BaseStreamReaderMixin):
    @property
    def delay(self):
        return 1.0 / self.sample_rate * self.samples_per_packet / 1.25

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

    def _pack_data(self, data, data_len, num_columns, samples_per_packet, start_index):

        start = start_index * self.data_byte_size * num_columns

        if samples_per_packet + start_index > data_len:
            end_index = data_len - (start_index + samples_per_packet)
            end = end_index * self.data_byte_size * num_columns

            return data[start:] + data[:end], end_index

        else:
            end_index = start_index + samples_per_packet
            end = end_index * self.data_byte_size * num_columns
            return data[start:end], end_index

    def read_device_config(self):

        config = get_test_device_configs(self.device_id)

        self._validate_config(config)

        return config

    def _read_source(self):
        print("Starting to read source test")
        index = 0

        data, data_len = self._generate_samples(
            len(self.config_columns), self.sample_rate
        )

        self.streaming = True

        if self.run_sml_model:
            sml = self.get_sml_model_obj()
        else:
            sml = None

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

                if self.run_sml_model:
                    self.execute_run_sml_model(sml, sample_data)

            except Exception as e:
                self.disconnect()
                raise e

            incycle = time.time() - incycle

            time.sleep(sleep_time - incycle)


class TestResultReader(TestReader, BaseResultReaderMixin):
    def set_app_config(self, config):
        config["DATA_SOURCE"] = self.name
        config["DEVICE_ID"] = self.device_id

    def _read_source(self):

        self.streaming = True

        while self.streaming:

            import random

            result = json.dumps(
                self._map_classification(
                    {"ModelNumber": 0, "Classification": random.randint(0, 10)}
                )
            )
            # Randomly removes a character to simulate dropped packets
            # index = random.randint(0, len(result) - 1)
            # result = result[:index] + result[index + 1 :]
            self.rbuffer.update_buffer([result, result])
            time.sleep(2)


def get_test_device_configs(device_id):

    config = {}

    if device_id == "Test IMU 6-axis Float":
        config["column_location"] = {
            "AccelerometerX": 0,
            "AccelerometerY": 1,
            "AccelerometerZ": 2,
            "GyroscopeX": 3,
            "GyroscopeY": 4,
            "GyroscopeZ": 5,
        }
        config["sample_rate"] = 119
        config["samples_per_packet"] = 6
        config["data_type"] = "float"

    elif device_id == "Test IMU 6-axis":
        config["column_location"] = {
            "AccelerometerX": 0,
            "AccelerometerY": 1,
            "AccelerometerZ": 2,
            "GyroscopeX": 3,
            "GyroscopeY": 4,
            "GyroscopeZ": 5,
        }
        config["sample_rate"] = 119
        config["samples_per_packet"] = 6
        config["data_type"] = "int16"

    elif device_id == "Test IMU 3-axis":
        config["column_location"] = {
            "AccelerometerX": 0,
            "AccelerometerY": 1,
            "AccelerometerZ": 2,
        }
        config["sample_rate"] = 119
        config["samples_per_packet"] = 6
        config["data_type"] = "int16"

    elif device_id == "Test Audio":
        config["column_location"] = {"Microphone": 0}
        config["sample_rate"] = 16000
        config["samples_per_packet"] = 480

    elif device_id == "Test IMU 9-axis float":
        config["column_location"] = {
            "AccelerometerX": 0,
            "AccelerometerY": 1,
            "AccelerometerZ": 2,
            "GyroscopeX": 3,
            "GyroscopeY": 4,
            "GyroscopeZ": 5,
            "X": 6,
            "Y": 7,
            "Z": 8,
        }
        config["sample_rate"] = 119
        config["samples_per_packet"] = 6
        config["data_type"] = "float"

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
