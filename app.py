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
import sys
import json

app = Flask(__name__)

app.config["SECRET_KEY"] = "any secret string"
app.config["CONFIG_SAMPLE_RATE"] = 100
app.config["CONFIG_SAMPLES_PER_PACKET"] = 10
app.config['DATA_SOURCE'] = None
app.config["CONFIG_COLUMNS"] = None
app.config["SERIAL_PORT"] = None
app.config["BLE_DEVICE_ID"] = None
app.config["STREAMING_SOURCE"] = None


# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

def cache_config(config):
    tmp = {"CONFIG_SAMPLE_RATE": app.config['CONFIG_SAMPLE_RATE'],
            "DATA_SOURCE":app.config['DATA_SOURCE'],
            "CONFIG_COLUMNS":app.config["CONFIG_COLUMNS"],
            "BLE_DEVICE_ID":app.config["BLE_DEVICE_ID"],
            "SERIAL_PORT":app.config['SERIAL_PORT'],            
           }
    json.dump(tmp, open('config.cache','w'))

@app.route("/")
def main():
    """Renders a sample page."""
    return render_template('index.html', source=app.config['DATA_SOURCE'], streaming=True if app.config['STREAMING_SOURCE'] else False, configuration=parse_current_config())


def parse_current_config():

    ret = {}
    ret["sample_rate"] = app.config["CONFIG_SAMPLE_RATE"]
    ret["column_location"] = dict()
    ret["samples_per_packet"] = app.config["CONFIG_SAMPLES_PER_PACKET"]
    ret["source"] = app.config['DATA_SOURCE']

    if app.config['CONFIG_COLUMNS']:
        for y in range(0, len(app.config["CONFIG_COLUMNS"])):
            if app.config["CONFIG_COLUMNS"].get(y, None):
                ret["column_location"][app.config["CONFIG_COLUMNS"][y]] = y
            else:
                ret["column_location"][app.config["CONFIG_COLUMNS"][str(y)]] = int(y)
    else:
        ret["column_location"] = {}

    return ret

@app.route("/config")
def get_config():

    ret = parse_current_config()

    return Response(dumps(ret), mimetype="application/json")



@app.route("/config-test", methods=["GET", "POST"])
def config_test():

    app.config['DATA_SOURCE'] = "TEST"

    source = get_source(app.config)

    source.set_config(app.config)

    source.send_connect()

    cache_config(app.config)

    return redirect("/")


@app.route("/config-serial", methods=["GET", "POST"])
def config_serial():
    form = SerialPortForm()

    app.config['DATA_SOURCE'] = "SERIAL"
    source = get_source(app.config)

    if request.method == "POST":

        source._port = form.data["serial_port"]

        source.set_config(app.config)
        print("STREAMING APP CONFIGURED FOR STREAMING")

        cache_config(app.config)

        return redirect("/")


    return render_template(
        "serialport.html", form=form, serial_port_list=source.list_available_devices()
    )


@app.route("/config-ble", methods=["GET", "POST"])
def config_ble():
    form = BLEDeviceListForm()

    app.config['DATA_SOURCE'] = "BLE"

    if request.method == "POST":

        app.config['BLE_DEVICE_ID'] = form.data["ble_device_id"]

        source = get_source(app.config)

        source.set_config(app.config)
        print("BLE APP CONFIGURED FOR STREAMING")

        source.disconnect()
        print("DISCONNECT FROM DEVICE")

        cache_config(app.config)

        return redirect("/")

    device_id_list = get_source(app.config, connect=False).list_available_devices()

    return render_template(
        "ble-device-list.html", form=form, ble_device_id_list=device_id_list
    )


@app.route("/stream")
def stream():

    if app.config.get("STREAMING_SOURCE", None):
        print("Source is already Streaming!")
        return "Source is already Streaming. Call disconnect to stop."

    source = get_source(app.config)

    app.config['STREAMING_SOURCE'] = source

    return Response(stream_with_context(source.read_data()), mimetype="application/octet-stream")



@app.route("/disconnect")
def disconnect():

    source = app.config.get('STREAMING_SOURCE', None)

    if source is not None:
        source.disconnect()

    del app.config['STREAMING_SOURCE']
    app.config['STREAMING_SOURCE'] = None
        
    return redirect("/")


if __name__ == "__main__":
    import os

    HOST = os.environ.get("SERVER_HOST", "localhost")
    try:
        PORT = int(os.environ.get("SERVER_PORT", "5555"))
    except ValueError:
        PORT = 5555

    if os.path.exists('config.cache'):
        app.config.update(json.load(open('config.cache','r')))

    app.run(HOST, 5555)
