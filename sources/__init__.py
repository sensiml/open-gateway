from sources.ble import BLEReader, BLEResultReader
from sources.test import TestReader, TestResultReader
from sources.serial import SerialReader, SerialResultReader
from sources.tcpip import TCPIPReader, TCPIPResultReader


def get_source(config, data_source, device_id, source_type="STREAMING", **kwargs):

    data_source = data_source.upper()
    print(data_source)

    if source_type == "STREAMING":
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

