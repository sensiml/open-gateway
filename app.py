"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import (
    render_template,
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
from forms import SerialPortForm, BLEDeviceListForm
from sources import get_source


app = Flask(__name__)

app.config["SECRET_KEY"] = "any secret string"
app.config["CONFIG_SAMPLE_RATE"] = 100
app.config["CONFIG_SAMPLES_PER_PACKET"] = 10
app.config['DATA_SOURCE'] = None
app.config["CONFIG_COLUMNS"] = None


# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route("/")
def main():
    """Renders a sample page."""
    return render_template('index.html')


@app.route("/config")
def return_config():

    ret = {}
    ret["sample_rate"] = app.config["CONFIG_SAMPLE_RATE"]
    ret["column_location"] = dict()
    ret["samples_per_packet"] = app.config["CONFIG_SAMPLES_PER_PACKET"]
    ret["source"] = app.config['DATA_SOURCE']

    if app.config['CONFIG_COLUMNS']:
        for y in range(0, len(app.config["CONFIG_COLUMNS"])):
            ret["column_location"][app.config["CONFIG_COLUMNS"][y]] = y
    else:
        ret["column_location"] = {}

    return Response(dumps(ret), mimetype="application/json")



@app.route("/config-dummy", methods=["GET", "POST"])
def config_dummy():

    app.config['DATA_SOURCE'] = "DUMMY"

    source = get_source(app.config)

    source.set_config(app.config)

    source.send_connect()

    return redirect("/config")


@app.route("/config-serial", methods=["GET", "POST"])
def serial_port():
    form = SerialPortForm()

    app.config['DATA_SOURCE'] = "SERIAL"
    source = get_source(app.config)

    if request.method == "POST":

        source._port = form.data["serial_port"]
        source.set_config(app.config)
        source.send_connect()

        return redirect("/config")


    return render_template(
        "serialport.html", form=form, serial_port_list=source.list_available_devices()
    )


@app.route("/config-ble", methods=["GET", "POST"])
def ble_config():
    form = BLEDeviceListForm()

    app.config['DATA_SOURCE'] = "BLE"
    source = get_source(app.config)


    if request.method == "POST":

        source._port = form.data["ble_device_id"]
        source.set_config(app.config)
        source.send_connect()

        return redirect("/config")


    return render_template(
        "ble-device-list.html", form=form, ble_device_id_list=source.list_available_devices()
    )


@app.route("/stream")
def stream():

    source = get_source(app.config)

    print(source.read_data())

    return Response(stream_with_context(source.read_data()), mimetype="application/octet-stream")


if __name__ == "__main__":
    import os

    HOST = os.environ.get("SERVER_HOST", "localhost")
    try:
        PORT = int(os.environ.get("SERVER_PORT", "5555"))
    except ValueError:
        PORT = 5555
    app.run(HOST, 5555)
