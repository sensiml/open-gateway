from sources.ble import BLEReader
from sources.test import TestReader
from sources.serial import SerialReader


def get_source(config, **kwargs):
    if config['DATA_SOURCE'] == 'TEST':
        return TestReader(config, **kwargs)

    if config['DATA_SOURCE'] == 'SERIAL':
        return SerialReader(config, **kwargs)

    if config['DATA_SOURCE'] == "BLE":
        return BLEReader(config, **kwargs)

    raise Exception("Invalid Data Source {}".format(config['DATA_SOURCE']))