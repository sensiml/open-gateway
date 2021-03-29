import serial.tools.list_ports
import json
import struct
import math
import time
import random
from sources.base import BaseReader, BaseResultReaderMixin, BaseStreamReaderMixin
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
            try:
                return value.decode("ascii")
            except:
                return None

    def _read_serial_buffer(self, buffer_size):
        with serial.Serial(self.port, self.baud_rate, timeout=1) as ser:
            return ser.read(buffer_size)

    def _flush_buffer(self):
        with serial.Serial(self.port, self.baud_rate, timeout=1) as ser:
            return ser.reset_input_buffer()

    def get_port_info(self):
        ports = serial.tools.list_ports.comports()

        port_list = []
        for index, (port, desc, hwid) in enumerate(sorted(ports)):
            port_list.append({"id": index, "name": desc, "device_id": port})

        return port_list

    def list_available_devices(self):
        return self.get_port_info()


class SerialStreamReader(SerialReader, BaseStreamReaderMixin):
    def _send_subscribe(self):
        self._write("connect")

    def read_device_config(self):

        config = json.loads(self._read_line())
        if self._validate_config(config):
            return config

        raise Exception("Invalid Configuration File")

    def _read_source(self):

        try:
            with serial.Serial(self.port, self.baud_rate, timeout=1) as ser:

                self.streaming = True
                ser.reset_input_buffer()

                while self.streaming:
                    data = ser.read(self.source_buffer_size)

                    self.buffer.update_buffer(data)

                    time.sleep(0.00001)

        except Exception as e:
            print(e)
            self.disconnect()
            raise e

    def set_app_config(self, config):

        config["DATA_SOURCE"] = "SERIAL"
        config["SOURCE_SAMPLES_PER_PACKET"] = self.source_samples_per_packet
        config["CONFIG_COLUMNS"] = self.config_columns
        config["CONFIG_SAMPLE_RATE"] = self.sample_rate
        config["DEVICE_ID"] = self.port


class SerialResultReader(SerialReader, BaseResultReaderMixin):
    def set_app_config(self, config):
        config["DATA_SOURCE"] = "SERIAL"
        config["DEVICE_ID"] = self.port

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
    connect(port)
    for i in range(1000):
        start = time.time()
        print(struct.unpack("h" * buffer_size, _get_serial_data(port, buffer_size)))
        print(time.time() - start)
