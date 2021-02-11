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

        super(TCPIPReader, self).__init__(config, device_id, **kwargs)

    @property
    def address(self):
        return "http://{}{}".format(self._address, self._port)

    @property
    def port(self):
        return self._port

    def read_config(self):

        r = requests.get("{}/config".format(self.address))

        return self._validate_config(r.json())

    def _read_source(self):

        url = "{}/{}".format(self.address, "stream")

        s = requests.Session()

        with s.get(url, headers=None, stream=True) as resp:
            for line in resp.iter_content():

                if not self.streaming:
                    return

                self._update_buffer(line)

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
    def set_config(self, config):
        config["DATA_SOURCE"] = "TCPIP"
        config["TCPIP"] = self.device_id
        print("config set")

    def _read_source(self):

        url = "{}/{}".format(self.address, "results")

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
                    self._update_result_buffer(content)
                    content = ""
                elif data == "{":
                    content = data
                else:
                    content += data


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

