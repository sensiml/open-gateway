import serial.tools.list_ports
import json
import struct
import math
import time
import random
from sources.base import BaseReader
import threading

BAUD_RATE = 460800


class SerialReader(BaseReader):
    def __init__(self, config, device_id, **kwargs):
        self._port = device_id
        self._baud_rate = config.get("BAUD_RATE", BAUD_RATE)

        super(SerialReader, self).__init__(config, device_id, **kwargs)

    @property
    def port(self):
        return self._port

    @property
    def baud_rate(self):
        return self._baud_rate

    def _write(self, command):
        with serial.Serial(self.port, self.baud_rate, timeout=1) as ser:
            ser.write(str.encode(command))

    def _read_line(self):
        with serial.Serial(self.port, self.baud_rate, timeout=1) as ser:
            value = ser.readline()
            if value:
                return value.decode("ascii")
            return None

    def _read_serial_buffer(self, buffer_size):
        with serial.Serial(self.port, self.baud_rate, timeout=1) as ser:
            return ser.read(buffer_size)

    def _flush_buffer(self):
        with serial.Serial(self.port, self.baud_rate, timeout=1) as ser:
            return ser.reset_input_buffer()

    def read_config(self):

        return {"sample_rate":16000, "samples_per_packet":240, "column_location":{"Microphone":0}}

        config = json.loads(self._read_line())
        if self._validate_config(config):
            return config

        raise Exception("Invalid Configuration File")

    def get_port_info(self):
        ports = serial.tools.list_ports.comports()

        port_list = []
        for index, (port, desc, hwid) in enumerate(sorted(ports)):
            port_list.append({"id": index, "name": desc, "device_id": port})

        return port_list

    def list_available_devices(self):
        return self.get_port_info()

    def send_subscribe(self):
        self._write("connect")

    def _read_source(self):


        with serial.Serial(self.port, self.baud_rate, timeout=1) as ser:

            self.streaming = True
            ser.reset_input_buffer()

            """
            start = time.time()
            buffer_size=0
            counter=0
            """

            while self.streaming:
                #incycle = time.time()
                data = ser.read(self.source_buffer_size)
                #print('time to read buffer: ', time.time()-incycle)
                self.buffer.update_buffer(data)
                """
                incycle = time.time()-incycle
                
                buffer_size+=len(data)
                counter+=1

                if time.time() - start > 1:
                    start = time.time()
                    counter = 0
                    buffer_size = 0

                print("time",  time.time() - start, "incycle", incycle,
                    'counter',counter,'buffer_size', buffer_size, 'source_buffer', self.source_buffer_size)
                """

    def set_config(self, config):

        source_config = self.read_config()

        self.data_width = len(source_config["column_location"])

        if not source_config:
            raise Exception("No configuration received from edge device.")
        self.source_samples_per_packet = source_config["samples_per_packet"]
        config["SOURCE_SAMPLES_PER_PACKET"] = self.source_samples_per_packet
        config["CONFIG_COLUMNS"] = source_config["column_location"]
        config["CONFIG_SAMPLE_RATE"] = source_config["sample_rate"]
        config["DATA_SOURCE"] = "SERIAL"
        config["SERIAL_PORT"] = self.port


class SerialResultReader(SerialReader):
    def set_config(self, config):
        config["DATA_SOURCE"] = "SERIAL"
        config["SERIAL_PORT"] = self.port

    def send_subscribe(self):
        pass

    def _read_source(self):

        self._flush_buffer()

        self.streaming = True
        while self.streaming:
            data = self._read_line()
            self.rbuffer.update_buffer([data])


if __name__ == "__main__":
    port = "/dev/ttyACM0"
    buffer_size = 6 * 10
    _get_serial_data(port, buffer_size)
    send_connect(port)
    for i in range(1000):
        start = time.time()
        print(struct.unpack("h" * buffer_size, _get_serial_data(port, buffer_size)))
        print(time.time() - start)
