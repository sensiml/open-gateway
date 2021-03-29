from bluepy.btle import Scanner, DefaultDelegate
from bluepy import btle
import struct
import sys
import json
import copy

try:
    from sources.base import BaseReader, BaseResultReaderMixin, BaseStreamReaderMixin
except:
    from base import BaseReader, BaseResultReaderMixin, BaseStreamReaderMixin
import time

uuidOfConfigChar = "16480001-0525-4ad5-b4fb-6dd83f49546b"
uuidOfDataChar = "16480002-0525-4ad5-b4fb-6dd83f49546b"
RecognitionClassUUID = "42421101-5A22-46DD-90F7-7AF26F723159"


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)


class StreamingDelegate(btle.DefaultDelegate):
    def __init__(self, lock):
        btle.DefaultDelegate.__init__(self)
        self.data = None
        self.new_data = False
        self._lock = lock

    def handleNotification(self, cHandle, value):

        with self._lock:

            if self.data:
                self.data += value
            else:
                self.data = value
            self.new_data = True


class ResultDelegate(StreamingDelegate):
    def handleNotification(self, cHandle, value):
        self.data = value


class BLEReader(BaseReader):
    """ Base Reader Object, describes the methods that must be implemented for each data source"""

    def __init__(self, config, device_id, connect=True, **kwargs):

        super(BLEReader, self).__init__(config, device_id, **kwargs)

        self.delegate = StreamingDelegate(self._lock)
        self.new_data = False
        self.data = []
        self.streaming = False
        self.subscribed = False
        self.peripheral = None

        if self.device_id and connect:
            self.peripheral = btle.Peripheral(self.device_id)
            print("getting characteristics")
            print(self.peripheral.getCharacteristics())
            self.peripheral.setDelegate(self.delegate)

    def disconnect(self):

        self.streaming = False
        self.subscribed = False

        if self.peripheral:
            try:
                self.peripheral.disconnect()
            except Exception as e:
                print(e)

        self._thread = None

        self.buffer.reset_buffer()
        self.rbuffer.reset_buffer()

    def list_available_devices(self):

        scanner = Scanner().withDelegate(ScanDelegate())
        devices = scanner.scan(5.0)

        device_list = []

        for index, dev in enumerate(devices):
            tmp = {"id": index, "device_id": dev.addr, "name": ""}
            for (adtype, desc, value) in dev.getScanData():
                if desc == "Complete Local Name":
                    tmp["name"] = value

            device_list.append(tmp)

        return device_list

    def read_device_config(self):

        print("reading config")
        if self.peripheral is None:
            raise Exception("BLE Device ID Not Configured.")

        source_config = self.peripheral.getCharacteristics(uuid=uuidOfConfigChar)[
            0
        ].read()

        return self._validate_config(
            json.loads(source_config.decode("ascii").rstrip("\x00"))
        )


class BLEStreamReader(BLEReader, BaseStreamReaderMixin):
    def _send_subscribe(self):

        if not self.subscribed:
            print("subscrbing")
            setup_data = b"\x01\x00"
            notify_handle = (
                self.peripheral.getCharacteristics(uuid=uuidOfDataChar)[0].getHandle()
                + 1
            )
            self.peripheral.writeCharacteristic(
                notify_handle, setup_data, withResponse=True
            )
            self.subscribed = True

    def _read_source(self):

        self.streaming = True

        # clear ble buffer
        self.delegate.new_data = False
        self.delegate.data = b""

        try:
            while self.streaming:

                if self.peripheral.waitForNotifications(0.01):
                    continue

                if self.delegate.new_data:
                    with self._lock:
                        tmp = copy.deepcopy(self.delegate.data)
                        self.delegate.new_data = False
                        self.delegate.data = b""

                    self.buffer.update_buffer(tmp)
                    time.sleep(0.00001)

        except Exception as e:
            print(e)
            self.disconnect()
            raise e

        print("streaming source stopped")

    def set_app_config(self, config):

        config["SOURCE_SAMPLES_PER_PACKET"] = self.source_samples_per_packet
        config["CONFIG_COLUMNS"] = self.config_columns
        config["CONFIG_SAMPLE_RATE"] = self.sample_rate
        config["DATA_SOURCE"] = "BLE"
        config["DEVICE_ID"] = self.device_id


class BLEResultReader(BLEReader, BaseResultReaderMixin):
    """ Base Reader Object, describes the methods that must be implemented for each data source"""

    def __init__(self, config, device_id, connect=True, **kwargs):

        super(BLEReader, self).__init__(config, device_id, **kwargs)

        self.delegate = ResultDelegate(self._lock)
        self.new_data = False
        self.data = []
        self.streaming = False
        self.subscribed = False
        self.device_id = device_id

        if self.device_id and connect:
            self.peripheral = btle.Peripheral(self.device_id)
            self.peripheral.setDelegate(self.delegate)

    def read_device_config(self):

        return {"samples_per_packet": 1}

    def set_app_config(self, config):
        config["DATA_SOURCE"] = "BLE"
        config["DEVICE_ID"] = self.device_id

    def _send_subscribe(self):

        print("sending connect")
        if not self.subscribed:
            print("subscring")
            setup_data = b"\x01\x00"
            notify_handle = (
                self.peripheral.getCharacteristics(uuid=RecognitionClassUUID)[
                    0
                ].getHandle()
                + 1
            )
            self.peripheral.writeCharacteristic(
                notify_handle, setup_data, withResponse=True
            )
            self.subscribed = True
            print("subscribed")

    def _read_source(self):

        self.streaming = True

        while self.streaming:
            if self.peripheral.waitForNotifications(0.1):
                continue
            if self.delegate.data is not None:
                if len(self.delegate.data) > 4:
                    print("ERROR HERE FOR SOME REASON")
                    raise Exception(
                        "Length of Delegeate data larger than a signle packet {}".format(
                            len(self.delegate.data)
                        )
                    )

                tmp = struct.unpack("h" * 2, self.delegate.data)
                self.delegate.data = None
                print("recieved classification", tmp)
                self.rbuffer.update_buffer(
                    [json.dumps({"ModelNumber": tmp[0], "Classification": tmp[1]})]
                )


if __name__ == "__main__":

    config = {
        "DATA_SOURCE": "BLE",
        "CONFIG_SAMPLE_RATE": 119,
        "CONFIG_SAMPLES_PER_PACKET": 10,
        "SOURCE_SAMPLES_PER_PACKET": 1,
        "DEVICE_ID": "dd:6c:dc:c1:99:fb",
        "CONFIG_COLUMNS": {
            "GyroscopeZ": 5,
            "AccelerometerX": 0,
            "AccelerometerY": 1,
            "GyroscopeX": 3,
            "AccelerometerZ": 2,
            "GyroscopeY": 4,
        },
        "CLASS_MAP": {},
    }

    device_id = "dd:6c:dc:c1:99:fb"
    device_id = "e0:17:52:fd:15:ab"

    """
    ble = BLEReader(config, device_id=device_id)
    ble.set_app_config(config)
    ble._send_subscribe()

    ble._read_source()
    """

    config["CONFIG_SAMPLES_PER_PACKET"] = 1

    ble = BLEResultReader(config, device_id=device_id)
    ble.update_config(config)
    ble.connect()
    ble.read_data()
