import serial
import serial.tools.list_ports
import time
import json
from collections import namedtuple

Header = namedtuple("Header", ["data_size", "rsvd", "channel", "sequence_number"])


def get_config(port: str, baud_rate: int):
    with serial.Serial(port, baud_rate, timeout=1) as ser:
        ser.write(b"disconnect")
        time.sleep(1)
        ser.readline()
        value = ser.readline().decode("ascii")

        return json.loads(value)


def get_port_info():
    ports = serial.tools.list_ports.comports()

    port_list = []
    for index, (port, desc, hwid) in enumerate(sorted(ports)):
        port_list.append({"id": index, "name": desc, "device_id": port})

    return port_list


class RecordSensor(object):
    """
    def append_channel_1(data):

        with open(data_file_1, "a") as file1:
            for item in data:
                file1.write(str(item) + "\n")

        sf.write("channel1.wav", np.array(data, dtype=np.int16), 16000)

        return len(data)
    """

    def __init__(self, file_prefix: str, port: str, baud_rate: int):
        self.file_prefix = file_prefix
        self.channel_data = []
        self.config = get_config(port, baud_rate)
        self.data = {}

    def write_buffer(self, channel: int):

        num_cols = self.data[channel]["num_columns"]
        data = self.data[channel]["data_buffer"]
        print(
            "writing channel",
            channel,
            "data size",
            len(data),
            "to",
            self.data[channel]["filename"],
        )
        with open(self.data[channel]["filename"], "a") as fid:

            for i in range(len(data) // num_cols):
                fid.write(
                    ",".join(
                        [str(data[i * num_cols + num_cols]) for i in range(num_cols)]
                    )
                    + "\n"
                )

        self.data[channel]["data_buffer"] = []

        return len(data) // num_cols

    def write_buffers(self):
        data_size = {}
        for channel in self.data:
            data_size[channel] = self.write_buffer(channel)

        return data_size

    @staticmethod
    def get_packet_header(ser):

        # Get size
        byte_array = ser.read() + ser.read()

        data_size = int.from_bytes(byte_array, "little")

        # get rsvd
        byte_array = ser.read()
        rsvd = int.from_bytes(byte_array, "little")

        byte_array = ser.read()
        channel = int.from_bytes(byte_array, "little")

        # read sequence number
        byte_array = ser.read() + ser.read() + ser.read() + ser.read()

        sequence_number = int.from_bytes(byte_array, "little")

        return Header(data_size, rsvd, channel, sequence_number)

    def get_packet_data(self, ser: serial, header: Header):

        for i in range((header.data_size - 6) // 2):
            byte_array = ser.read() + ser.read()
            data_point = int.from_bytes(byte_array, "little", signed="True")
            self.data[header.channel]["data_buffer"].append(data_point)

    def find_sync(self, ser: serial):
        found_sync = False
        while not found_sync:
            char_in = ser.read()
            if char_in == b"\xff":
                found_sync = True

    def get_packets(self, ser: serial):
        self.find_sync(ser)
        header = self.get_packet_header(ser)
        self.get_packet_data(ser, header)
        data_byte = ser.read()
        checksum = int.from_bytes(data_byte, "little")

    def connect(self, record_time: int, port: str, baud_rate: int):
        with serial.Serial(port, baud_rate, timeout=1) as ser:
            ser.reset_input_buffer()
            print("Connecting")
            ser.write(b"connect")
            start = time.time()

            print("Recording for", record_time, "seconds")
            print(0)
            curr_time = 0
            while record_time > time.time() - start:
                if int(time.time() - start) != curr_time:
                    curr_time = int(time.time() - start)
                    if curr_time % 5 == 0:
                        print(curr_time)

                self.get_packets(ser)
            print(curr_time)
            record_time = time.time() - start

            ser.write(b"disconnect")

            return record_time

    def init(self):
        for sensor_config in self.config["sensors"]:
            filename = "{prefix}_channel{index}.csv".format(
                prefix=self.file_prefix, index=sensor_config["channel"]
            )
            with open(filename, "w") as out:
                out.write(",".join(sensor_config["column_location"].keys()))

            self.data[sensor_config["channel"]] = {
                "filename": filename,
                "data_buffer": [],
                "num_columns": len(sensor_config["column_location"]),
                "sample_rate": sensor_config["sample_rate"],
            }


def summarize_recording(data_sizes, recorder):
    for channel in data_sizes.keys():
        print(
            "channel",
            channel,
            "record_time",
            record_time,
            "recorded",
            int(recorded_time),
            "expected",
            record_time * recorder.data[channel]["sample_rate"],
            "actual",
            data_sizes[channel],
            "calculated",
            int(data_sizes[channel] / recorded_time),
        )


if __name__ == "__main__":

    COM_PORT = "COM4"
    RECORD_TIME = 10
    BAUD_RATE = 921600

    if not COM_PORT:
        port_list = get_port_info()
        COM_PORT = port_list[0]["device_id"]

    config = get_config(COM_PORT, BAUD_RATE)

    print("Retrieved Config")
    print(json.dumps(config, indent=4, sort_keys=True))

    filenames = []

    recorder = RecordSensor("test", COM_PORT, BAUD_RATE)
    recorder.init()

    record_time = RECORD_TIME
    recorded_time = recorder.connect(record_time, COM_PORT, BAUD_RATE)
    data_sizes = recorder.write_buffers()

    summarize_recording(data_sizes, recorder)
