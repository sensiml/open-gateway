import json
import struct
import math
import time
import random
import requests
import threading
import copy
from sources.base import BaseReader

WIFI_PORT = ":80"


class TCPIPReader(BaseReader):
    def __init__(self, config, device_id, **kwargs):

        self.device_id = device_id

        if kwargs.get("connect", True) is True:

            self._address = device_id.split(":")[0]

            if len(device_id.split(":")) == 2:
                self._port = ":" + device_id.split(":")[1]
            else:
                self._port = WIFI_PORT

            self._init_buffer()

        super(TCPIPReader, self).__init__(config, **kwargs)

    def _init_buffer(self):
        self._data_buffer_1 = b""
        self._data_buffer_2 = b""
        self._data_buff = 1

    @property
    def address(self):
        return "http://{}{}".format(self._address, self._port)

    @property
    def port(self):
        return self._port

    def read_config(self):
        r = requests.get("{}/config".format(self.address))

        return self._validate_config(r.json())

    def list_available_devices(self):
        return []

    def _update_buffer(self, data):

        if self._data_buff == 1:
            self._data_buffer_1 += data
        if self._data_buff == 2:
            self._data_buffer_2 += data

    def _read_buffer(self, buffer_size):

        if self._data_buff == 1:
            if len(self._data_buffer_1) < buffer_size:
                return
            self._data_buffer_2 = self._data_buffer_1[buffer_size:]
            self._data_buff = 2
            tmp = copy.deepcopy(self._data_buffer_1[:buffer_size])
            self._data_buffer_1 = b""

            return tmp

        if self._data_buff == 2:
            if len(self._data_buffer_2) < buffer_size:
                return
            self._data_buffer_1 = self._data_buffer_2[buffer_size:]
            self._data_buff = 1
            tmp = copy.deepcopy(self._data_buffer_2[:buffer_size])
            self._data_buffer_2 = b""
            return tmp

    def _read_stream(self, path):

        url = "{}/{}".format(self.address, path)

        s = requests.Session()

        with s.get(url, headers=None, stream=True) as resp:
            for line in resp.iter_content():

                if not self.streaming:
                    return

                self._update_buffer(line)

    def _read_sensor_data(self):
        return self._read_stream("stream")

    def read_data(self):

        if self.device_id is None:
            raise Exception("IP Adress not configured!")

        if self.streaming:
            pass
        else:
            self._thread = threading.Thread(target=self._read_sensor_data)
            self.streaming = True
            self._thread.start()
            print("starting thread")

        while self.streaming:

            data = self._read_buffer(self.packet_buffer_size)

            if data:
                yield data

    def set_config(self, config):

        source_config = self.read_config()

        self.data_width = len(source_config["column_location"])

        if not source_config:
            raise Exception("No configuration received from edge device.")

        config["CONFIG_COLUMNS"] = source_config["column_location"]
        config["CONFIG_SAMPLE_RATE"] = source_config["sample_rate"]
        config["DATA_SOURCE"] = "TCPIP"
        config["TCPIP"] = self.device_id


class TCPIPResultReader(TCPIPReader):
    def _init_buffer(self):
        self._data_buffer_1 = []
        self._data_buffer_2 = []
        self._data_buff = 1

    def set_config(self, config):
        config["DATA_SOURCE"] = "TCPIP"
        config["TCPIP"] = self.device_id
        print("config set")

    def send_connect(self):
        pass

    def _update_buffer(self, data):

        if self._data_buff == 1:
            self._data_buffer_1.append(data)
        if self._data_buff == 2:
            self._data_buffer_2.append(data)

    def _read_buffer(self):

        if self._data_buff == 1:
            self._data_buff = 2
            tmp = copy.deepcopy(self._data_buffer_1)
            self._data_buffer_1 = []
            return tmp

        if self._data_buff == 2:
            self._data_buff = 1
            tmp = copy.deepcopy(self._data_buffer_2)
            self._data_buffer_2 = []
            return tmp

    def _read_line(self, path):

        url = "{}/{}".format(self.address, path)

        s = requests.Session()

        with s.get(url, headers=None, stream=True) as resp:
            content = ""

            for cont in resp.iter_content():
                if not self.streaming:
                    return

                try:
                    data = cont.decode("ascii")
                except Exception as e:
                    print(e)
                    continue

                if data == "}":
                    content += data
                    self._update_buffer(content)
                    content = ""
                elif data == "{":
                    content = data
                else:
                    content += data

    def _read_results(self):
        return self._read_line("results")

    def read_data(self):

        if self.device_id is None:
            raise Exception("IP Adress not configured!")

        if self.streaming:
            pass
        else:
            self._thread = threading.Thread(target=self._read_results)
            self.streaming = True
            self._thread.start()

        while self.streaming:
            data = self._read_buffer()
            for result in data:
                if self._validate_results_data(result):
                    result = self._map_classification(json.loads(result))
                    yield json.dumps(result) + "\n"


if __name__ == "__main__":
    device_id = "192.168.86.27:80"
    config = {
        "CONFIG_SAMPLES_PER_PACKET": 10,
        "CONFIG_SAMPLE_RATE": 100,
        "CONFIG_COLUMNS": ["X", "Y", "Z"],
    }

    import threading
    import time

    """
    reader =  TCPResultReader(config, device_id)
    """

    reader = TCPIPReader(config, device_id)

    print(reader.read_config())
    # print(reader._read_sensor_data())

    for data in reader.read_data():
        print(data)

