import json
import copy
import threading
import array
import struct
import time
import csv
import os
from sources.base import BaseReader, BaseStreamReaderMixin, BaseResultReaderMixin

try:
    from sources.buffers import CircularBufferQueue, CircularResultsBufferQueue
except:
    from buffers import CircularBufferQueue, CircularResultsBufferQueue
SHORT = 2


class BaseFusionReader(BaseReader):
    """ Base Reader Object, describes the methods that must be implemented for each data source"""

    def __init__(self, sources, device_id):
        self.sources = sources
        self.bindex = [False for _ in range(len(self.sources))]
        self.device_id = device_id
        self.samples_per_packet = 1
        self.recording = False
        self._record_thread = None

    @property
    def num_sources(self):
        return len(self.sources)

    @property
    def streaming(self):
        return self.is_streaming()

    def is_recording(self):
        return self.recording

    def connect(self):
        for source in self.sources:
            source.connect()

    def disconnect(self):
        for source in self.sources:
            source.disconnect()

    def _check_streaming(self):
        for source in self.sources:
            if not source.streaming:
                return False

        return True

    def is_streaming(self):
        return self._check_streaming()


class FusionStreamReader(BaseFusionReader, BaseStreamReaderMixin):
    def read_config(self):

        for source in self.sources:
            source.read_config()

        config = {}
        sample_rates = set()
        samples_per_packet = set()
        combined_samples_per_packet = 0
        config_columns = set()
        combined_config_columns = {}
        for index, source in enumerate(self.sources):
            sample_rates.add(source.sample_rate)
            samples_per_packet.add(source.samples_per_packet)
            config_columns.add(len(source.config_columns))
            combined_samples_per_packet += source.samples_per_packet
            combined_config_columns.update(
                {
                    "S_{}_{}".format(index, k): v + len(combined_config_columns)
                    for k, v in source.config_columns.items()
                }
            )

        if len(sample_rates) != 1:
            raise Exception("All sources must have the same sample rate.")

        if len(samples_per_packet) != 1:
            raise Exception("All sources must have the same samples per packet.")

        if len(config_columns) != 1:
            raise Exception("All sources must have the same number of channels.")

        config["sample_rate"] = sample_rates.pop()
        config["samples_per_packet"] = combined_samples_per_packet
        config["column_location"] = combined_config_columns

        self.source_samples_per_packet = config["samples_per_packet"]
        self.sample_rate = config["sample_rate"]
        self.config_columns = config.get("column_location")

        return config

    def set_app_config(self, config):

        config["SOURCE_SAMPLES_PER_PACKET"] = self.source_samples_per_packet
        config["CONFIG_COLUMNS"] = self.config_columns
        config["CONFIG_SAMPLE_RATE"] = self.sample_rate
        config["DEVICE_ID"] = self.device_id

    def _check_is_ready(self):
        for index, source in enumerate(self.sources):
            self.bindex[index] = source.buffer.get_latest_buffer()
            if self.bindex[index] is None:
                return False

        return True

    def read_data(self):

        data = [[] for _ in range(self.num_sources)]
        data_ready = [False] * self.num_sources

        while self.is_streaming():
            if self._check_is_ready():
                break
            time.sleep(0.01)

        while self.is_streaming():

            for index, source in enumerate(self.sources):
                if not data_ready[index] and source.buffer.is_buffer_full(
                    self.bindex[index]
                ):
                    data[index] = source.buffer.get_buffer_iterator(
                        self.bindex[index], source.data_width
                    )
                    data_ready[index] = True
                    self.bindex[index] = source.buffer.get_next_index(
                        self.bindex[index]
                    )

                if is_data_ready(data_ready):
                    yield inerleave_buffers(data)
                    data_ready = [False] * self.num_sources

            time.sleep(0.001)

        print("stream ended")
        yield None


def inerleave_buffers(data_buffers):

    packet_buffer = b""

    getting_packets = True

    while getting_packets:
        for index, packet in enumerate(data_buffers):

            tmp = next(packet)

            if tmp:
                packet_buffer += tmp
            else:
                getting_packets = False

    return packet_buffer


def is_data_ready(data_ready):
    for data in data_ready:
        if not data:
            return False

    return True


if __name__ == "__main__":

    from test import TestStreamReader

    config = {"CONFIG_SAMPLES_PER_PACKET": 1}

    t1 = TestStreamReader(config, "Test IMU 6-axis")
    t2 = TestStreamReader(config, "Test IMU 6-axis")
    t3 = TestStreamReader(config, "Test IMU 6-axis")

    f = FusionReader([t1, t2, t3])

    f.read_config()
    f.set_app_config(config)

    f.connect()

    print("Start to read data")

    # for f in f.read_data():
    #    print(f)

    f.disconnect()
