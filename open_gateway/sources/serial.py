import serial.tools.list_ports
import json
import struct
import math
import time
import random
import threading


from open_gateway.sources.base import (
    BaseReader,
    BaseResultReaderMixin,
    BaseStreamReaderMixin,
)

BAUD_RATE = 460800


class SerialReader(BaseReader):
    name = "SERIAL"

    def __init__(self, config, device_id, **kwargs):

        super(SerialReader, self).__init__(config, device_id, **kwargs)
        self._port = device_id
        self._baud_rate = config.get("BAUD_RATE", BAUD_RATE)
        self._streaming_version = 1
        print("BAUD rate set to", self._baud_rate)

    @property
    def port(self):
        return self._port

    @property
    def baud_rate(self):
        return self._baud_rate
    
    @property
    def streaming_version(self):
        return self._streaming_version

    def _write(self, command):
        with serial.Serial(self.port, self.baud_rate, timeout=1) as ser:
            ser.write(str.encode(command))

    def _read_line(self, flush_buffer=False):
        with serial.Serial(self.port, self.baud_rate, timeout=1) as ser:

            value = ser.readline()
            if flush_buffer:
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

        try:
            config = json.loads(self._read_line(flush_buffer=True))
            self._streaming_version = config.get("version", 1)
            
            print("Serial Streaming Version: ", self.streaming_version)
            
            if not self.streaming_version in [1,2]:
                raise Exception(f"Invalid Streaming Version: {self.streaming_version}")
        except:
            self._write("disconnect")
            time.sleep(1.0)
            config = json.loads(self._read_line(flush_buffer=True))

        if self._validate_config(config):
            return config

        raise Exception("Invalid Configuration File")
    
    def _find_head_version_2(self, ser):
        
        data_block_byte_length = self.packet_buffer_size + 6
        data_block_size_code = data_block_byte_length.to_bytes(2, 'little')
        reserved_byte_code = b'\x00'
        sync_byte_code = b'\xff'
        
        # maximum number of iterations to locate the start of the data packet
        max_try = 10000
        
        sync_byte = ser.read()
        for i in range(max_try):
            while (sync_byte != sync_byte_code):
                sync_byte = ser.read()
            
            # read in 3 bytes: LL + R
            lenght_reserved_bytes = ser.read(3)
            if lenght_reserved_bytes != data_block_size_code + reserved_byte_code:
                sync_byte = ser.read()
                continue
            else:
                break
        
        if i == max_try - 1:
            raise Exception(f"Could not find data packet header, streaming version: {self.streaming_version}") 
        
        # read the packet data until it ends
        ser.read(data_block_byte_length)
        
        
    def _read_serial_data(self, ser):
        
        if self.streaming_version == 1:
            sensor_data = ser.read(self.source_buffer_size)
        elif self.streaming_version == 2:
            overhead_size = 10
            packet_data = ser.read(self.packet_buffer_size + overhead_size)
            sensor_data = packet_data[9:-1]
            
        return sensor_data
    
        

    def _read_source(self):

        try:
            print("Serial: Reading source stream")
            with serial.Serial(self.port, self.baud_rate, timeout=1) as ser:

                self.streaming = True
                ser.reset_input_buffer()
                ser.read(self.source_buffer_size)

                if self.run_sml_model:
                    sml = self.get_sml_model_obj()
                else:
                    sml = None
                
                if self.streaming_version == 1:
                    pass  
                elif self.streaming_version == 2:
                    self._find_head_version_2(ser)
                

                while self.streaming:
                    
                    data = self._read_serial_data(ser) 
                    self.buffer.update_buffer(data)

                    if self.run_sml_model:
                        model_result = self.execute_run_sml_model(sml, data)
                        if model_result:
                            self.rbuffer.update_buffer([model_result])                        

                    time.sleep(0.00001)

                print("Serial: Sending disconnect command")
                ser.write(str.encode("disconnect"))

        except Exception as e:
            print(e)
            self.disconnect()
            raise e


class SerialResultReader(SerialReader, BaseResultReaderMixin):
    def set_app_config(self, config):
        config["DATA_SOURCE"] = self.name
        config["DEVICE_ID"] = self.port

    def _read_source(self):

        self._flush_buffer()

        self.streaming = True
        with serial.Serial(self.port, self.baud_rate, timeout=1) as ser:
            while self.streaming:
            
                try:
                    value = ser.readline()                    
                    data = [value.decode("ascii")]
                    
                except Exception as e:
                    print(e,)
                    print("value", value)
                    continue

                
                if "ModelNumber" in data[0]:
                    self.rbuffer.update_buffer(data)
                elif data[0]:
                    print(data[0].rstrip())


if __name__ == "__main__":
    port = "/dev/ttyACM0"
    buffer_size = 6 * 10
    config={'DATA_SOURCE':'RESULTS', "DEVICE_ID":"COM4"}
    sr = SerialResultReader(config, "COM4")
    sr.connect()
    sr._read_source()