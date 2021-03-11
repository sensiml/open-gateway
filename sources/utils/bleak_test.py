import asyncio
import time
from bleak import BleakScanner, BleakClient


async def scan():
    devices = await BleakScanner.discover()

    for d in devices:
        print(d)

    return devices


def callback(sender, data):
    print(sender, data)


async def connect_to_device(address, charUUID):
    async with BleakClient(address, timeout=1.0) as client:
        print("connect to", address)
        try:
            await client.start_notify(charUUID, callback)
            await asyncio.sleep(10.0)
        except Exception as e:
            print(e)

    print("disconnect from", address)


async def read_gatt(address, charUUID):
    print("Reading Gat")
    async with BleakClient(address) as client:
        x = await client.is_connected()
        print("here")
        resp = await client.read_gatt_char(charUUID)
        print(resp)


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    devices = loop.run_until_complete(scan())

    address = "DB:E2:5F:47:EC:42"

    uuidOfConfigChar = "16480001-0525-4ad5-b4fb-6dd83f49546b"
    uuidOfDataChar = "16480002-0525-4ad5-b4fb-6dd83f49546b"

    # loop.run_until_complete(read_gatt(address, uuidOfConfigChar))

    # time.sleep(10)
    print("connecting")
    task1 = asyncio.create_task(connect_to_device(address, uuidOfDataChar))

    asyncio.run(task1)

