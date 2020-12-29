from bluepy.btle import Scanner, DefaultDelegate
from bluepy import btle
import struct
import sys
import json
import copy
from sources.base import BaseReader
import time

uuidOfConfigChar = "16480001-0525-4ad5-b4fb-6dd83f49546b"
uuidOfDataChar = "16480002-0525-4ad5-b4fb-6dd83f49546b"

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)


class MyDelegate(btle.DefaultDelegate):
    def __init__(self, params):
        btle.DefaultDelegate.__init__(self)
        self.data  = None
        self.new_data = False

    def handleNotification(self, cHandle, value):
        #print(struct.unpack("h"*6,value))
        #print(len(value), value)
        if self.data:
            self.data += value
        else:
            self.data = value
        self.new_data = True

class BLEReader(BaseReader):
    """ Base Reader Object, describes the methods that must be implemented for each data source"""

    def __init__(self, config, connect=True, **kwargs):

        self.delegate = MyDelegate(None)
        self.new_data = False
        self.data = []
        self.streaming = False
        self.subscribed = False
        self.device_id = config.get('BLE_DEVICE_ID', None)

        if self.device_id and connect:
            self.peripheral = btle.Peripheral(self.device_id)
            self.peripheral.setDelegate(self.delegate)

        super(BLEReader, self).__init__(config, **kwargs)


    def disconnect(self):
        self.streaming=False
        self.subscribed = True
        
        self.peripheral.disconnect()

    def list_available_devices(self):

        scanner = Scanner().withDelegate(ScanDelegate())
        devices = scanner.scan(5.0)

        device_list = []

        for dev in devices:
            s =  "Device ID: %s - " % (dev.addr)
            for (adtype, desc, value) in dev.getScanData():
                if desc == 'Complete Local Name':
                    s += " Name = %s" % (value)

            device_list.append(s)

        return device_list

    def send_connect(self):

        if not self.subscribed:
            setup_data = b"\x01\x00"
            notify_handle = self.peripheral.getCharacteristics(uuid=uuidOfDataChar)[0].getHandle() + 1
            self.peripheral.writeCharacteristic(notify_handle, setup_data, withResponse=True)
            self.subscribed = True

    def read_config(self):

        source_config = self.peripheral.getCharacteristics(uuid=uuidOfConfigChar)[0].read()
        return json.loads(source_config.decode('ascii').rstrip('\x00'))

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
        config["DATA_SOURCE"] = "BLE"

        self._data_width = len(config_columns)

    def read_data(self):

        self.send_connect()
        time.sleep(1)

        self.streaming=True

        while self.streaming:
            if self.peripheral.waitForNotifications(.01):
                continue
            if self.delegate.new_data:
                tmp = copy.deepcopy(self.delegate.data)
                if len(tmp) >= self.packet_buffer_size:
                    self.delegate.new_data=False
                    self.delegate.data=self.delegate.data[self.packet_buffer_size:]
                    
                    yield tmp[:self.packet_buffer_size]            


if __name__ == "__main__":

    config = {"CONFIG_COLUMNS": [] ,
              "CONFIG_SAMPLE_RATE": [],
              "DATA_SOURCE":'BLE',
            }

    ble = BLEReader({})
    ble.set_config(config)
    ble.send_connect()

    for i in ble.read_data():
        print(i)