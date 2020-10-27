"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, Response, stream_with_context
import time
from json import dumps
import random, struct
import math

#this instruction can only be used with IPython Notbook.
# showing the exact location of the smaples

app = Flask(__name__)

app.config["CONFIG_COLUMNS"] = ["AccelerometerX", "AccelerometerY", "AccelerometerZ", "GyroscopeX", "GyroscopeY", "GyroscopeZ"]
app.config["CONFIG_SAMPLE_RATE"] = 1000
app.config["CONFIG_SAMPLES_PER_PACKET"] = 100
INT16_BYTE_SIZE = 2


# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

gen_data = dict()
def _generate_samples():

    fs = 16000
    f = app.config["CONFIG_SAMPLE_RATE"] # the frequency of the signal

    x = list(range(0,fs)) # the points on the x axis for plotting
    # compute the value (amplitude) of the sin wave at the for each sample

    for y in range(0, len(app.config["CONFIG_COLUMNS"])):
        new_amp = random.randint(200,32768)
        axis_data = [ new_amp * math.sin(2*math.pi*f * (xs/fs)) for xs in x]
        gen_data[app.config["CONFIG_COLUMNS"][y]] = axis_data
    return gen_data

@app.route('/')
def hello():
    """Renders a sample page."""
    return "Hello World!"


@app.route("/config")
def return_config():
    ret = {}
    ret["sample_rate"] = app.config.get("CONFIG_SAMPLE_RATE", 200)
    ret["column_location"] = dict()
    ret["samples_per_packet"] = app.config.get("CONFIG_SAMPLES_PER_PACKET", 1)

    for y in range(0, len(app.config["CONFIG_COLUMNS"])):
        ret["column_location"][app.config["CONFIG_COLUMNS"][y]] = y
    return Response(dumps(ret), mimetype="application/json")

@app.route('/stream')
def stream():
    delay = (1.0/app.config["CONFIG_SAMPLE_RATE"]) * app.config["CONFIG_SAMPLES_PER_PACKET"]/1.25
    byteSize = len(app.config["CONFIG_COLUMNS"]) * app.config["CONFIG_SAMPLES_PER_PACKET"] * INT16_BYTE_SIZE

    print("Delay {}, ByteArray size: {}".format(delay, byteSize))
    num_cols = len(app.config["CONFIG_COLUMNS"])
    def gen():
        try:
            i = 0
            while True:
                sample_data = bytearray(byteSize)
                for x in range(0, app.config["CONFIG_SAMPLES_PER_PACKET"]):
                    for y in range(0, num_cols):
                        struct.pack_into('<h', sample_data, (y+(x*num_cols))*2, int(gen_data[app.config["CONFIG_COLUMNS"][y]][i]))
                    i = i + 1
                    if i == len(gen_data[app.config["CONFIG_COLUMNS"][0]]):
                        i = 0
                yield bytes(sample_data)

                time.sleep(delay)
        except GeneratorExit:
            print('closed')

    return Response(stream_with_context(gen()), mimetype="application/octet-stream")


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    _generate_samples()
    app.run(HOST, 5555)


