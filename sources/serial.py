import serial.tools.list_ports
import json
import struct
import math
import time
import random
from sources.base import BaseReader

SHORT = 2
BAUD_RATE = 921600

class SerialReader(BaseReader):

    def __init__(self, config, **kwargs):
        self._port = config.get('SERIAL_PORT', None)
        self._baud_rate = config.get('BAUD_RATE', BAUD_RATE)
        self._buffer_size = None
        self._data_width = len(config.get("CONFIG_COLUMNS", []))

    @property
    def port(self):
        return self._port

    @property
    def baud_rate(self):
        return self.baud_rate

    @property
    def data_width(self):
        return self._data_width

    def _write(self, command):
        with serial.Serial(self.port, self.baud_rate, timeout=1) as ser:
            ser.write(command)

    def _read_line(self):
        with serial.Serial(self.port, self.baud_rate, timeout=1) as ser:
            return ser.readline()


    def _read_buffer(self,buffer_size):
        with serial.Serial(self.port, self.baud_rate, timeout=1) as ser:
            return ser.read(SHORT * buffer_size)


    def _flush_buffer(self):
        with serial.Serial(self.port, self.baud_rate, timeout=1) as ser:
            return ser.reset_input_buffer()

    def read_config(self):
        try:
            source_config = json.loads(read_line())
        except:
            return {}


    def get_port_info(self):
        ports = serial.tools.list_ports.comports()

        port_list = []
        for index, (port, desc, hwid) in enumerate(sorted(ports)):
            port_list.append("{}. Description: {}, Port: {}".format(index, desc, port))

        return port_list

    def list_available_devices(self):
        return self.get_port_info()

    def set_config(self, config):

        source_config = self.read_config()

        if not source_config:
            raise Exception("Invalid Source Configuration")

        config_columns = {}
        config_coumns = ["" for x in range(len(source_config["column_location"]))]
        for key, value in source_config["column_location"].items():
            config_columns[value] = key

        config["CONFIG_COLUMNS"] = config_columns
        config["CONFIG_SAMPLE_RATE"] = source_config["sample_rate"]
        config["DATA_SOURCE"] = "SERIAL"
        config["SERIAL_PORT"] = self.port

        self._data_width = len(config_columns)


    def send_connect(self):
        self._write("connect")

    def read_data(self, samples_per_packet):

        if self.port is None:
            return "Serial Port not configured!"

        self._flush_buffer()

        while True:
            yield self._read_buffer(
                self.data_width
                * samples_per_packet,
            )



if __name__ == "__main__":
    port = "/dev/ttyACM0"
    buffer_size = 6 * 10
    _get_serial_data(port, buffer_size)
    send_connect(port)
    for i in range(1000):
        start = time.time()
        print(struct.unpack("h" * buffer_size, _get_serial_data(port, buffer_size)))
        print(time.time() - start)
