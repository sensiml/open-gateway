from bluepy.btle import Scanner, DefaultDelegate
from bluepy import btle
import struct
import sys
from sources.base import BaseReader

data = []
new_data = False

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


    def handleNotification(self, cHandle, data):
        print(struct.unpack("h"*6,data))
        data.append(struct.unpack("h"*6,data))
        new_data = True



class BLEReader(BaseReader):
    """ Base Reader Object, describes the methods that must be implemented for each data source"""

    def __init__(self, config, **kwargs):


        self.device_id =  "dd:6c:dc:c1:99:fb" #config.get('BLE_DEVICE_ID', None)

        if self.device_id:
            self.peripheral = btle.Peripheral(self.device_id)
            self.peripheral.setDelegate(MyDelegate(0))

    def read_config(self):
        pass

    def list_available_devices(self):

        scanner = Scanner().withDelegate(ScanDelegate())
        devices = scanner.scan(5.0)

        device_list = []

        for dev in devices:
            s =  "Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi)
            for (adtype, desc, value) in dev.getScanData():
                s += "  %s = %s" % (desc, value)

            device_list.append(s)

        return device_list

    def send_connect(self):

        setup_data = b"\x01\x00"
        notify_handle = self.getCharacteristics(uuid=uuidOfDataChar)[0].getHandle() + 1
        self.peripheral.writeCharacteristic(notify_handle, setup_data, withResponse=True)

    def set_config(self, config):
        source_config = self.peripheral.getCharacteristics(uuid=uuidOfConfigChar)[0].read()

        print(source_config)

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
        while True:
            if p.waitForNotifications(.01):
                continue
            if new_data:
                tmp = copy.deepcopy(data)
                new_data=Falsse
                data=[]
                yield tmp
