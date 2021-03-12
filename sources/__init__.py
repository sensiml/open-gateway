import sys
from sources.test import TestStreamReader, TestResultReader
from sources.serial import SerialStreamReader, SerialResultReader
from sources.tcpip import TCPIPStreamReader, TCPIPResultReader
from sources.fusion import FusionStreamReader, FusionResultReader

if sys.platform not in ["win32", "darwin"]:
    from sources.ble import BLEStreamReader, BLEResultReader
else:
    from sources.ble_bleak import BLEStreamReader, BLEResultReader


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
        return FusionStreamReader(config, sources, device_ids)
    else:
        return FusionResultReader(config, sources, device_ids)


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
