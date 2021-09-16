import sys
from open_gateway.sources.test import TestStreamReader, TestResultReader
from open_gateway.sources.serial import SerialStreamReader, SerialResultReader
from open_gateway.sources.tcpip import TCPIPStreamReader, TCPIPResultReader
from open_gateway.sources.fusion import FusionStreamReader, FusionResultReader


try:
    # use bleak ble drivers
    from open_gateway.sources.ble_bleak import BLEStreamReader, BLEResultReader
except:
    # use bluepy ble driver
    from open_gateway.sources.ble import BLEStreamReader, BLEResultReader


def get_fusion_source(
    config, data_source, device_ids, source_type="DATA_CAPUTRE", **kwargs
):
    """ Allows you to combine multiple sources into a single synced stream for Data Capture"""
    sources = []
    for index, device_id in enumerate(device_ids.split(",")):

        sources.append(
            get_source(
                config, data_source, device_id, source_type=source_type, **kwargs
            )
        )

    if source_type == "DATA_CAPTURE":
        return FusionStreamReader(config, sources, device_ids, data_source)
    else:
        return FusionResultReader(config, sources, device_ids, data_source)


def get_source(config, data_source, device_id, source_type="DATA_CAPTURE", **kwargs):

    if device_id and len(device_id.split(",")) > 1:
        return get_fusion_source(
            config, data_source, device_id, source_type=source_type, **kwargs
        )

    data_source = data_source.upper()

    if source_type == "DATA_CAPTURE":
        if data_source == "TEST":
            return TestStreamReader(config, device_id, **kwargs)

        if data_source == "SERIAL":
            return SerialStreamReader(config, device_id, **kwargs)

        if data_source == "BLE":
            return BLEStreamReader(config, device_id, **kwargs)

        if data_source == "TCPIP":
            return TCPIPStreamReader(config, device_id, **kwargs)

    if source_type == "RECOGNITION":
        if data_source == "BLE":
            return BLEResultReader(config, device_id, **kwargs)

        if data_source == "SERIAL":
            return SerialResultReader(config, device_id, **kwargs)

        if data_source == "TEST":
            return TestResultReader(config, device_id, **kwargs)

        if data_source == "TCPIP":
            return TCPIPResultReader(config, device_id, **kwargs)

    print(source_type, data_source)
    raise Exception("Invalid Data Source {}".format(data_source))
