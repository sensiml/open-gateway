import json
import struct
import math
import time
import random
from base import BaseReader
import requests

WIFI_PORT = 80


class TCPReader(BaseReader):
    def __init__(self, config, device_id, **kwargs):
        self.device_id = device_id
        self._address = device_id.split(':')[0]
        self._port = device_id.split(':')[1]
        self._data_buffer_1 = b""
        self._data_buffer_2 = b""
        self._data_buff = 1

        super(TCPReader, self).__init__(config, **kwargs)

    @property
    def address(self):
        return "http://{}:{}".format(self._address, self._port)

    @property
    def port(self):
        return self._port

    def read_config(self):
        r = requests.get('{}/config'.format(self.address))

        return self._validate_config(r.json())

    def get_port_info(self):
        return {}

    def list_available_devices(self):
        return self.get_port_info()

    def _read_stream(self, path):

        url = '{}/{}'.format(self.address, path)

        s = requests.Session()

        with s.get(url, headers=None, stream=True) as resp:
            s = b""
            counter = 0
            for line in resp.iter_content():
                s+=line
                counter+=1

                if counter%7*10==0:
                    if self._data_buff==1:
                        self._data_buffer_1 += s
                    else
                        self._data_buffer_2 += s
                
                
    def _read_sensor_data(self):
        return self._read_stream('stream')

    def read_data(self):

        if self._address is None:
            raise Exception("IP Address is not configured!")

        self.streaming = True

        while self.streaming:
            if self._data_buff==1:
                self._data_buffer_2=b""
                self._data_buff=2
                yield self._data_buffer_1                
            else:
                self._data_buffer_1=b""
                self._data_buff=1
                self._data_buffer_1
                yield self._data_buffer_2


    def set_config(self, config):

        source_config = self.read_config()

        self.data_width = len(source_config["column_location"])

        if not source_config:
            raise Exception("No configuration received from edge device.")

        config["CONFIG_COLUMNS"] = source_config["column_location"]
        config["CONFIG_SAMPLE_RATE"] = source_config["sample_rate"]
        config["DATA_SOURCE"] = "TCPIP"
        config["TCPIP"] = self.device_id



class TCPResultReader(TCPReader):

    def set_config(self, config):
        config["DATA_SOURCE"] = "TCPIP"
        config["TCPIP"] = self.device_id

    def send_connect(self):
        pass

    def _read_results(self):
        return self._read_stream('results')

    def read_data(self):

        if self.device_id is None:
            raise Exception("IP Adress not configured!")

        self.streaming = True
        while self.streaming:
            data = self._read_results()

            print(data)
            if self._validate_results_data(data):
                yield data


if __name__ == "__main__":
    device_id = "192.168.86.249:80"
    config = {'CONFIG_SAMPLES_PER_PACKET':10, "CONFIG_SAMPLE_RATE":100}

    import threading
    import time

    #reader =  TCPResultReader(config, device_id)
    #reader._read_results()

    reader = TCPReader(config, device_id)
    print(reader.read_config())
    #print(reader._read_sensor_data())
    print(reader.read_data())