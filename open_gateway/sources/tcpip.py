import json
import struct
import math
import time
import random
import requests
import threading
import copy
from open_gateway.sources.base import (
    BaseReader,
    BaseResultReaderMixin,
    BaseStreamReaderMixin,
)

WIFI_PORT = ":80"


class TCPIPReader(BaseReader):
    name = "TCPIP"

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


class TCPIPStreamReader(TCPIPReader, BaseStreamReaderMixin):
    def read_device_config(self):
        r = requests.get("{}/config".format(self.address))

        return self._validate_config(r.json())

    def _read_source(self):
        try:
            url = "{}/{}".format(self.address, "stream")

            s = requests.Session()

            self.streaming = True

            if self.run_sml_model:
                sml = self.get_sml_model_obj()
            else:
                sml = None

            with s.get(url, headers=None, stream=True) as resp:
                for data in resp.iter_content(chunk_size=self.source_buffer_size):
                    if not self.streaming:
                        return

                    self.buffer.update_buffer(data)

                    if self.run_sml_model:
                        model_result = self.execute_run_sml_model(sml, data)
                        if model_result:
                            self.rbuffer.update_buffer([model_result])

                    time.sleep(0.0001)

        except Exception as e:
            print(e)
            self.disconnect()
            raise e


class TCPIPResultReader(TCPIPReader, BaseResultReaderMixin):
    def set_app_config(self, config):
        config["DATA_SOURCE"] = self.name
        config["DEVICE_ID"] = self.device_id

    def _read_source(self):
        url = "{}/{}".format(self.address, "results")

        s = requests.Session()

        self.streaming = True

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
                    self.rbuffer.update_buffer([content])
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
