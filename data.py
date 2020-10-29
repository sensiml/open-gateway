import serial.tools.list_ports
import json
import struct
import math
import time
import random

SHORT=2
BAUD_RATE=921600

def _generate_samples(num_columns, sample_rate):
    fs = sample_rate*10
    f = sample_rate 

    x = list(range(0,fs)) # the points on the x axis for plotting

    return [[ 1000*offset + 1000*math.sin(2*math.pi*f * (float(xs)/fs)) for xs in x] for offset in range(num_columns)]
    

def pack_data(data, byteSize, samples_per_packet, start_index):
    sample_data = bytearray(byteSize)
    num_cols = len(data)
    data_len = len(data[0])
    end_index = start_index + samples_per_packet
    if end_index > data_len:
        end_index -= data_len
        
    for x in range(0, samples_per_packet):
        if x+start_index >= data_len:
            start_index = 0
        for y in range(0, num_cols):
            struct.pack_into('<h', sample_data, (y+(x*num_cols))*2, random.randint(-50,50)+int(data[y][x+start_index]))


    return bytes(sample_data), end_index

def get_port_info():
    ports = serial.tools.list_ports.comports()

    port_list = []
    for index, (port, desc, hwid) in enumerate(sorted(ports)):
        port_list.append("{}. Description: {}, Port: {}".format(index, desc, port))

    return port_list

def read_line(port):
    with serial.Serial(port, BAUD_RATE, timeout=1) as ser:
        return ser.readline()

def read_buffer(port, buffer_size):
    with serial.Serial(port, BAUD_RATE, timeout=1) as ser:
        return ser.read(SHORT*buffer_size)

def check_for_config(port, default_config):
    try:
        config = json.loads(read_line(port))
    except:
        config = default_config

    config_columns = {}
    config_coumns = ["" for x in range(len(config['column_location']))]
    for key, value in config['column_location'].items():
        config_columns[value] = key

    config["CONFIG_COLUMNS"] = config_columns
    return config

def send_connect(port):
    with serial.Serial(port, BAUD_RATE, timeout=1) as ser:
        ser.write('connect')

def _get_serial_data(port, buffer_size):
    data = read_buffer(port, buffer_size)
    #udata = struct.unpack('h'*buffer_size, data)
    #print(utdata)

    return data

if __name__ == "__main__":
    port= "/dev/ttyACM0"
    buffer_size=6*10
    _get_serial_data(port,buffer_size)
    send_connect(port)
    for i in range(1000):
        start = time.time()
        print(struct.unpack('h'*buffer_size, _get_serial_data(port, buffer_size)))
        print(time.time() - start)
