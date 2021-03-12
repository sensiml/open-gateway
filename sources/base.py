import json
import copy
import threading
import array
import struct
import time
import csv
import os

try:
    from sources.buffers import CircularBufferQueue, CircularResultsBufferQueue
except:
    from buffers import CircularBufferQueue, CircularResultsBufferQueue
SHORT = 2


class BaseReader(object):
    """ Base Reader Object, describes the methods that must be implemented for each data source"""

    def __init__(self, config, device_id=None, name=None, **kwargs):
        self.samples_per_packet = config["CONFIG_SAMPLES_PER_PACKET"]
        self.class_map = config["CLASS_MAP"]
        self.loop = config["LOOP"]
        self.name = name
        self.source_samples_per_packet = None
        self.sample_rate = None
        self.config_columns = None
        self.device_id = device_id
        self.recording = False
        self.streaming = False
        self._thread = None
        self._record_thread = None
        self.buffer = None
        self.rbuffer = None
        self._lock = threading.Lock()

    @property
    def data_width(self):
        if self.config_columns is None:
            return 0

        return len(self.config_columns)

    @property
    def packet_buffer_size(self):
        return self.samples_per_packet * self.source_buffer_size

    @property
    def source_buffer_size(self):
        if self.source_samples_per_packet is None:
            return 2
        return self.source_samples_per_packet * self.data_width * SHORT

    @staticmethod
    def _validate_config(config):

        if not isinstance(config, dict):
            raise Exception("Invalid Configuration")

        if config.get("column_location", None) is None:
            raise Exception("Invalid Configuration: no column_location")
        if config.get("sample_rate", None) is None:
            raise Exception("Invalid Configuration: no sample_rate")
        if config.get("samples_per_packet", None) is None:
            raise Exception("Invalid Configuration: no samples_per_packet")

        return config

    @staticmethod
    def _validate_results_data(data):
        try:
            tmp = json.loads(data)
            if isinstance(tmp, dict) and tmp:
                return True
        except Exception as e:
            print(e)

        return False

    def is_recording(self):
        return self.recording

    def is_streaming(self):
        return self.streaming

    def list_available_devices(self):
        return []

    def _send_subscribe(self):
        pass

    def read_config(self):
        """ read the config from the device and set the properties of the object """

        config = self.read_device_config()

        self.source_samples_per_packet = config.get("samples_per_packet", None)
        self.sample_rate = config.get("sample_rate", None)
        self.config_columns = config.get("column_location", None)

        print("Setting Configuration")

        return config

    def update_config(self, config):
        """ update the objects local config values from the app cache """

        self.samples_per_packet = config["CONFIG_SAMPLES_PER_PACKET"]
        self.source_samples_per_packet = config["SOURCE_SAMPLES_PER_PACKET"]
        self.sample_rate = config["CONFIG_SAMPLE_RATE"]
        self.config_columns = config.get("CONFIG_COLUMNS")
        self.class_map = config.get("CLASS_MAP")

    def connect(self):

        if self._thread is None:
            "Assume if there is a thread, we are already connected"

            self.buffer = CircularBufferQueue(
                self._lock, buffer_size=self.packet_buffer_size
            )
            self.rbuffer = CircularResultsBufferQueue(self._lock, buffer_size=1)

            self._send_subscribe()

            time.sleep(1)

            self.buffer.reset_buffer()

            self._thread = threading.Thread(target=self._read_source)
            self._thread.start()

            time.sleep(1)

        else:
            print("Thread Already Started!")

    def disconnect(self):
        self.streaming = False
        self._thread = None
        self._record_thread = None
        self.recording = False

        self.buffer.reset_buffer()
        self.rbuffer.reset_buffer()

    def record_start(self, filename):

        if not self.streaming:
            raise Exception("Must start streaming before begging to record!")

        if self.recording:
            raise Exception("Only a single recording can occur at one time")

        if filename is None:
            raise Exception("Invalid Filename")

        if not os.path.exists(os.path.dirname(filename)):
            print(
                "File directory does not exist,  recording to data directory in gateway location."
            )
            if not os.path.exists("./data"):
                os.mkdir("./data")

            filename = os.path.join("./data", os.path.basename(filename))

        self.recording = True
        self._record_thread = threading.Thread(
            target=self._record_data, kwargs={"filename": filename}
        )
        self._record_thread.start()

    def record_stop(self, filename=None):
        if self.recording != True:
            raise Exception("Not currently recording")

        self._record_thread = None
        self.recording = False

        return True


class BaseStreamReaderMixin(object):
    def read_data(self):
        """ Generator to read the data stream out of the buffer """

        print("starting read")

        if self._thread:
            pass
        else:
            print("sent connect")
            self.connect()
            self.streaming = True

        index = self.buffer.get_latest_buffer()

        while self.streaming:

            if index is None:
                index = self.buffer.get_latest_buffer()
                time.sleep(0.1)
                continue

            if self.buffer.is_buffer_full(index):
                data = self.buffer.read_buffer(index)
                index = self.buffer.get_next_index(index)

                if data:
                    yield data

            time.sleep(0.001)

        print("stream ended")

    def _record_data(self, filename):

        with open(filename + ".csv", "w", newline="") as csvfile:
            datawriter = csv.writer(csvfile, delimiter=",")
            print("Starting to Record .csv")

            datawriter.writerow(
                [
                    x[0]
                    for x in sorted(
                        self.config_columns.items(), key=lambda item: item[1]
                    )
                ]
            )
            struct_info = "h" * self.data_width

            data_reader = self.read_data()

            while self.recording:

                data = next(data_reader)

                if data:
                    for row_index in range(len(data) // (self.data_width * 2)):
                        buff_index = row_index * self.data_width * 2
                        datawriter.writerow(
                            struct.unpack(
                                struct_info,
                                data[buff_index : buff_index + self.data_width * 2],
                            )
                        )

        print("CSV recording thread finished")


class BaseResultReaderMixin(object):
    def read_device_config(self):
        print("here")
        return {"samples_per_packet": 1}

    def _map_classification(self, results):

        if self.class_map:
            results["Classification"] = self.class_map.get(
                results["Classification"], results["Classification"]
            )

        return results

    def read_data(self):
        """ Genrator to read the result stream out of the buffer """

        print("starting result read")

        if self._thread:
            pass
        else:
            print("sent connect")
            self.connect()

        index = self.rbuffer.get_latest_buffer()

        while self.streaming:

            if index is None:
                index = self.rbuffer.get_latest_buffer()
                time.sleep(0.1)
                continue

            if self.rbuffer.is_buffer_full(index):
                data = self.rbuffer.read_buffer(index)
                index = self.rbuffer.get_next_index(index)

                for result in data:
                    if self._validate_results_data(result):
                        result = self._map_classification(json.loads(result))
                        result["timestap"] = time.time()
                        print(result)
                        yield json.dumps(result) + "\n"

            else:
                time.sleep(0.1)

        print("result stream ended")

    def _record_data(self, filename):

        with open(filename + ".csv", "w", newline="") as out:
            data_reader = self.read_data()

            while self.recording:

                data = next(data_reader)

                if data:
                    out.write(data)

        print("recording thread finished")
