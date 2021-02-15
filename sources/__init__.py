import sys
from sources.test import TestReader, TestResultReader
from sources.serial import SerialReader, SerialResultReader
from sources.tcpip import TCPIPReader, TCPIPResultReader

if sys.platform not in ["win32", "darwin"]:
    from sources.ble import BLEReader, BLEResultReader
else:
    print("BLE is not supported on Windows!")


def get_source(config, data_source, device_id, source_type="DATA_CAPTURE", **kwargs):

    data_source = data_source.upper()

    if source_type == "DATA_CAPTURE":
        if data_source == "TEST":
            return TestReader(config, **kwargs)

        if data_source == "SERIAL":
            return SerialReader(config, device_id, **kwargs)

        if data_source == "BLE":
            return BLEReader(config, device_id, **kwargs)

        if data_source == "TCPIP":
            return TCPIPReader(config, device_id, **kwargs)

    if source_type == "RESULTS":
        if data_source == "BLE":
            return BLEResultReader(config, device_id, **kwargs)

        if data_source == "SERIAL":
            return SerialResultReader(config, device_id, **kwargs)

        if data_source == "TEST":
            return TestResultReader(config, **kwargs)

        if data_source == "TCPIP":
            return TCPIPResultReader(config, device_id, **kwargs)

    print(source_type, data_source)
    raise Exception("Invalid Data Source {}".format(data_source))
