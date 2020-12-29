from sources.ble import BLEReader
from sources.TEST import TestReader
from sources.serial import SerialReader


def get_source(config):
    if config['DATA_SOURCE'] == 'TEST':
        return TestReader(config)

    if config['DATA_SOURCE'] == 'SERIAL':
        return SerialReader(config)

    if config['DATA_SOURCE'] == "BLE":
        return BLEReader(config)

    raise Exception("Invalid Data Source {}".format(config['DATA_SOURCE']))