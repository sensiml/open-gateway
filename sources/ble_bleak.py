import asyncio
from bleak import BleakScanner, BleakClient
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


class BLEReader(BaseReader):
    """ Base Reader Object, describes the methods that must be implemented for each data source"""

    def __init__(self, config, device_id, connect=True, **kwargs):

        super(BLEReader, self).__init__(config, device_id, **kwargs)

        self.new_data = False
        self.data = []
        self.subscribed = False
        self.peripheral = None
        self.streaming = False

    def handleNotification(self, cHandle: int, value: bytearray):
        print(cHandle, value)

    @staticmethod
    async def read_gatt(address, charUUID):
        async with BleakClient(address) as client:
            x = await client.is_connected()
            resp = await client.read_gatt_char(charUUID)
            return resp

    @staticmethod
    async def runScanner():
        devices = await BleakScanner.discover()
        return devices

    async def connect_to_device(self, address):
        async with BleakClient(address, timeout=1.0) as client:
            print("connect to", address)
            self.streaming = True
            try:
                await client.start_notify(self.charUUID, self.handleNotification)
                while self.streaming:
                    await asyncio.sleep(0.25)
            except Exception as e:
                print(e)
                self.streaming = False
                await client.stop_notify(self.charUUID)

            self.streaming = False
            await client.stop_notify(self.charUUID)

        print("disconnect from", address)

    def disconnect(self):

        self.streaming = False
        self.subscribed = False

        time.sleep(1.0)

        self._thread = None

        self.buffer.reset_buffer()
        self.rbuffer.reset_buffer()

    def list_available_devices(self):

        devices = self.loop.run_until_complete(self.runScanner())
        print(devices)

        device_list = []

        for index, device in enumerate(devices):
            device_list.append(
                {"id": index, "device_id": device.address, "name": device.name}
            )

        return device_list

    def read_device_config(self):

        if self.device_id is None:
            raise Exception("BLE Device ID Not Configured.")

        source_config = self.loop.run_until_complete(
            self.read_gatt(address=self.device_id, charUUID=uuidOfConfigChar)
        )

        return self._validate_config(
            json.loads(source_config.decode("ascii").rstrip("\x00"))
        )

    def _read_source(self):

        self.streaming = True

        try:
            self.loop.run_until_complete(self.connect_to_device(self.device_id))
        except Exception as e:
            print(e)
            self.disconnect()
            raise e

        print("streaming source stopped")


class BLEStreamReader(BLEReader, BaseStreamReaderMixin):

    charUUID = uuidOfDataChar

    def handleNotification(self, cHandle: int, value: bytearray):
        self.buffer.update_buffer(value)

    def set_app_config(self, config):

        config["SOURCE_SAMPLES_PER_PACKET"] = self.source_samples_per_packet
        config["CONFIG_COLUMNS"] = self.config_columns
        config["CONFIG_SAMPLE_RATE"] = self.sample_rate
        config["DATA_SOURCE"] = "BLE"
        config["DEVICE_ID"] = self.device_id


class BLEResultReader(BLEReader, BaseResultReaderMixin):
    """ Base Reader Object, describes the methods that must be implemented for each data source"""

    charUUID = RecognitionClassUUID

    def read_device_config(self):

        return {"samples_per_packet": 1}

    def set_app_config(self, config):
        config["DATA_SOURCE"] = "BLE"
        config["DEVICE_ID"] = self.device_id

    def handleNotification(self, cHandle: int, value: bytearray):
        tmp = struct.unpack("h" * 2, value)
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
    device_id = "DB:E2:5F:47:EC:42"

    ble = BLEStreamReader(config, device_id=device_id)
    ble.set_app_config(config)

    print("connect")
    ble.connect()

    print("read_data")
    counter = 0
    for data in ble.read_data():
        print(data)
        counter += 1
        if counter == 200:
            break

    print("disconnecting")
    ble.disconnect()
    time.sleep(5)
    print("here")
    """

    config["CONFIG_SAMPLES_PER_PACKET"] = 1

    ble = BLEResultReader(config, device_id=device_id)
    ble.update_config(config)
    ble.connect()
    ble.read_data()
    """
