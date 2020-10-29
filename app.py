"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import (
    Flask,
    Response,
    stream_with_context,
    url_for,
    render_template,
    redirect,
    request,
)
import time
from json import dumps
import random, struct
import math
from forms import SerialPortForm
from data import (
    _generate_samples,
    get_port_info,
    pack_data,
    check_for_config,
    _get_serial_data,
    send_connect,
    _generate_samples,
    flush_buffer,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "any secret string"
app.config["CONFIG_COLUMNS"] = [
    "AccelerometerX",
    "AccelerometerY",
    "AccelerometerZ",
    "GyroscopeX",
    "GyroscopeY",
    "GyroscopeZ",
]
app.config["CONFIG_SAMPLE_RATE"] = 100
app.config["CONFIG_SAMPLES_PER_PACKET"] = 10
app.config["TEST"] = True
app.config["SERIAL_PORT"] = "/dev/ttyACM0"
INT16_BYTE_SIZE = 2

_config = {
    "sample_rate": 119,
    "serial_port": app.config["SERIAL_PORT"],
    "samples_per_packet": app.config["CONFIG_SAMPLES_PER_PACKET"],
    "column_location": {
        "AccelerometerY": 1,
        "AccelerometerX": 0,
        "GyroscopeZ": 5,
        "GyroscopeY": 4,
        "GyroscopeX": 3,
        "AccelerometerZ": 2,
    },
}

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route("/")
def main():
    """Renders a sample page."""
    return "Welcome to the SensiML IoT Streaming Server!"


@app.route("/config")
def return_config():
    ret = {}
    ret["sample_rate"] = app.config["CONFIG_SAMPLE_RATE"]
    ret["column_location"] = dict()
    ret["samples_per_packet"] = app.config["CONFIG_SAMPLES_PER_PACKET"]

    for y in range(0, len(app.config["CONFIG_COLUMNS"])):
        ret["column_location"][app.config["CONFIG_COLUMNS"][y]] = y

    return Response(dumps(ret), mimetype="application/json")


@app.route("/serialport", methods=["GET", "POST"])
def serial_port():
    form = SerialPortForm()
    if request.method == "POST":
        app.config["SERIAL_PORT"] = form.data["serial_port"]
        config = check_for_config(app.config["SERIAL_PORT"], _config)
        app.config["CONFIG_SAMPLE_RATE"] = config["sample_rate"]
        app.config["CONFIG_COLUMNS"] = config["CONFIG_COLUMNS"]
        app.config["TEST"] = False
        send_connect(app.config["SERIAL_PORT"])

        return redirect("/config")

    return render_template(
        "serialport.html", form=form, serial_port_list=get_port_info()
    )


@app.route("/stream")
def stream():

    delay = (
        (1.0 / app.config["CONFIG_SAMPLE_RATE"])
        * app.config["CONFIG_SAMPLES_PER_PACKET"]
        / 1.25
    )
    byteSize = (
        len(app.config["CONFIG_COLUMNS"])
        * app.config["CONFIG_SAMPLES_PER_PACKET"]
        * INT16_BYTE_SIZE
    )
    num_cols = len(app.config["CONFIG_COLUMNS"])

    def gen():
        if app.config["TEST"]:
            index = 0
            data = _generate_samples(num_cols, app.config["CONFIG_SAMPLE_RATE"])
            while True:
                sample_data, index = pack_data(
                    data, byteSize, app.config["CONFIG_SAMPLES_PER_PACKET"], index
                )
                yield sample_data
                time.sleep(delay)

        else:
            flush_buffer(app.config["SERIAL_PORT"])
            while True:
                yield _get_serial_data(
                    app.config["SERIAL_PORT"],
                    len(app.config["CONFIG_COLUMNS"])
                    * app.config["CONFIG_SAMPLES_PER_PACKET"],
                )

    return Response(stream_with_context(gen()), mimetype="application/octet-stream")


if __name__ == "__main__":
    import os

    HOST = os.environ.get("SERVER_HOST", "localhost")
    try:
        PORT = int(os.environ.get("SERVER_PORT", "5555"))
    except ValueError:
        PORT = 5555
    app.run(HOST, 5555)
