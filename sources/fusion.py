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

    def __init__(self,config, sources, device_id):
        self.class_map = config["CLASS_MAP"]
        self.samples_per_packet = config["CONFIG_SAMPLES_PER_PACKET"]
        self.sources = sources
        self.device_id = device_id
        self.source_samples_per_packet = 1
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


    def is_data_ready(self, data_ready):
        for data in data_ready:
            if not data:
                return False

        return True


    def _check_is_stream_source_ready(self, bindex):
        for index, source in enumerate(self.sources):
            bindex[index] = source.buffer.get_latest_buffer()
            if bindex[index] is None:
                return False

        return True



    def _check_is_result_source_ready(self, bindex):
        for index, source in enumerate(self.sources):
            bindex[index] = source.rbuffer.get_latest_buffer()
            if bindex[index] is None:
                return False

        return True


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


    def read_data(self):



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

        bindex = [False for _ in range(len(self.sources))]
        data = [[] for _ in range(self.num_sources)]
        data_ready = [False] * self.num_sources

        while self.is_streaming():
            if self._check_is_stream_source_ready(bindex):
                break
            time.sleep(0.01)

        while self.is_streaming():

            for index, source in enumerate(self.sources):
                if not data_ready[index] and source.buffer.is_buffer_full(
                    bindex[index]
                ):
                    data[index] = source.buffer.get_buffer_iterator(
                        self.bindex[index], source.data_width
                    )
                    data_ready[index] = True
                    bindex[index] = source.buffer.get_next_index(
                        bindex[index]
                    )

                if self.is_data_ready(data_ready):
                    yield inerleave_buffers(data)
                    data_ready = [False] * self.num_sources

            time.sleep(0.001)

        print("stream ended")
        yield None




class FusionResultReader(BaseFusionReader, BaseResultReaderMixin):


    def set_app_config(self, config):

        config["SOURCE_SAMPLES_PER_PACKET"] = self.samples_per_packet
        config["DEVICE_ID"] = self.device_id


    def read_data(self):


        bindex = [False for _ in range(len(self.sources))]
        data = [[] for _ in range(self.num_sources)]
        data_ready = [False] * self.num_sources

        while self.is_streaming():

            if self._check_is_result_source_ready(bindex):
                break
            time.sleep(0.01)

        while self.is_streaming():

            for index, source in enumerate(self.sources):
                if source.rbuffer.is_buffer_full(
                    bindex[index]
                ):

                    data[index] = source.rbuffer.read_buffer(bindex[index])
                    bindex[index] = source.rbuffer.get_next_index(bindex[index])
                    data_ready[index] = True


            for index, is_datain_ready in enumerate(data_ready):
                if is_datain_ready:
                    for result in data[index]:
                        if self._validate_results_data(result):
                            result = self.sources[index]._map_classification(json.loads(result))
                            result["timestap"] = time.time()
                            result['source'] = self.sources[index].device_id
                            result['name'] = self.sources[index].name
                            yield json.dumps(result) + "\n"
                    data_ready[index] = False


            time.sleep(0.001)

        print("stream ended")
        yield None

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
