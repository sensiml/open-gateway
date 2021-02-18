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
from json import dumps
from forms import DeviceConfigureForm, DeviceScanForm
from sources import get_source
import json
from flask_cors import CORS
from errors import errors

app = Flask(__name__, static_folder="./webui/build", static_url_path="/")
app.register_blueprint(errors)
CORS(app, resources={r"/*": {"origins": "*"}})


app.config["SECRET_KEY"] = "any secret string"
app.config["CONFIG_SAMPLE_RATE"] = None
app.config["CONFIG_SAMPLES_PER_PACKET"] = 10
app.config["DATA_SOURCE"] = None
app.config["CONFIG_COLUMNS"] = []
app.config["SERIAL_PORT"] = None
app.config["TCPIP"] = None
app.config["BLE_DEVICE_ID"] = None
app.config["STREAMING_SOURCE"] = None
app.config["RESULT_SOURCE"] = None
app.config["MODE"] = ""
app.config["STREAMING"] = False
app.config["BAUD_RATE"] = 460800
app.config["CLASS_MAP"] = None

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


def cache_config(config):
    tmp = {
        "CONFIG_SAMPLE_RATE": app.config["CONFIG_SAMPLE_RATE"],
        "DATA_SOURCE": app.config["DATA_SOURCE"],
        "CONFIG_COLUMNS": app.config["CONFIG_COLUMNS"],
        "BLE_DEVICE_ID": app.config["BLE_DEVICE_ID"],
        "SERIAL_PORT": app.config["SERIAL_PORT"],
        "MODE": app.config["MODE"],
        "TCPIP": app.config["TCPIP"],
    }
    json.dump(tmp, open("./.config.cache", "w"))


@app.route("/")
def main():
    return app.send_static_file("index.html")


def get_device_id():
    if app.config["DATA_SOURCE"] == "BLE":
        return app.config["BLE_DEVICE_ID"]
    if app.config["DATA_SOURCE"] == "SERIAL":
        return app.config["SERIAL_PORT"]
    if app.config["DATA_SOURCE"] == "TCPIP":
        return app.config["TCPIP"]
    else:
        return "TESTER"


def parse_current_config():

    ret = {}
    ret["sample_rate"] = app.config["CONFIG_SAMPLE_RATE"]
    ret["column_location"] = dict()
    ret["samples_per_packet"] = app.config["CONFIG_SAMPLES_PER_PACKET"]
    ret["source"] = app.config["DATA_SOURCE"]
    ret["device_id"] = get_device_id()
    ret["streaming"] = app.config["STREAMING"]
    ret["baud_rate"] = app.config["BAUD_RATE"]
    ret["mode"] = app.config["MODE"].lower()

    if app.config["CONFIG_COLUMNS"]:
        ret["column_location"] = app.config["CONFIG_COLUMNS"]
    else:
        ret["column_location"] = {}

    return ret


def get_config():

    ret = parse_current_config()

    return Response(dumps(ret), mimetype="application/json")


@app.route("/scan", methods=["POST"])
def scan():
    form = DeviceScanForm()

    print(form.data["source"].upper())

    source = get_source(
        app.config,
        device_id=None,
        data_source=form.data["source"].upper(),
        connect=False,
    )

    device_id_list = source.list_available_devices()

    return Response(json.dumps(device_id_list), mimetype="application/json")


@app.route("/connect", methods=["GET"])
def connect():

    if app.config["MODE"] == "DATA_CAPTURE":
        if app.config.get("STREAMING_SOURCE", None) is None:
            app.config["STREAMING_SOURCE"] = get_source(
                app.config,
                device_id=get_device_id(),
                data_source=app.config["DATA_SOURCE"],
                source_type="DATA_CAPTURE",
            )

            app.config.get("STREAMING_SOURCE").send_connect()

            app.config["STREAMING"] = True

    elif app.config["MODE"] == "RESULTS":
        if app.config.get("RESULTS_SOURCE", None) is None:
            app.config["RESULTS_SOURCE"] = get_source(
                app.config,
                device_id=get_device_id(),
                data_source=app.config["DATA_SOURCE"],
                source_type="RESULTS",
            )

            app.config["STREAMING"] = True

            app.config["RESULTS_SOURCE"].send_connect()

    return get_config()


@app.route("/config", methods=["GET", "POST"])
def config():
    form = DeviceConfigureForm()

    if request.method == "POST":
        disconnect()
        app.config["STREAMING"] = False

        source = get_source(
            app.config,
            data_source=form.data["source"].upper(),
            source_type="DATA_CAPTURE",
            device_id=form.data["device_id"],
        )

        print("SET CONFIG")
        source.set_config(app.config)

        print("SEND CONNECT")
        source.send_connect()
        app.config["STREAMING"] = True

        app.config["MODE"] = "DATA_CAPTURE"

        cache_config(app.config)

        app.config["STREAMING_SOURCE"] = source

        print(app.config)

    ret = parse_current_config()

    return Response(dumps(ret), mimetype="application/json")


@app.route("/config-results", methods=["GET", "POST"])
def config_results():
    form = DeviceConfigureForm()

    if request.method == "POST":
        disconnect()
        app.config["STREAMING"] = False

        source = get_source(
            app.config,
            data_source=form.data["source"].upper(),
            device_id=form.data["device_id"],
            source_type="RESULTS",
        )

        source.set_config(app.config)

        source.send_connect()

        app.config["STREAMING"] = True

        app.config["MODE"] = "RESULTS"

        app.config["RESULT_SOURCE"] = source

        cache_config(app.config)

        return get_config()

    ret = parse_current_config()

    return Response(dumps(ret), mimetype="application/json")


@app.route("/stream")
def stream():

    if app.config.get("STREAMING_SOURCE", None) is None:
        app.config["STREAMING_SOURCE"] = get_source(
            app.config,
            device_id=get_device_id(),
            data_source=app.config["DATA_SOURCE"],
            source_type="DATA_CAPTURE",
        )

        app.config["STREAMING"] = True
        print("source was none")

    return Response(
        stream_with_context(app.config["STREAMING_SOURCE"].read_data()),
        mimetype="application/octet-stream",
    )


@app.route("/results")
def results():

    if app.config.get("RESULT_SOURCE", None) is None:

        app.config["RESULT_SOURCE"] = get_source(
            app.config,
            device_id=get_device_id(),
            data_source=app.config["DATA_SOURCE"],
            source_type="RESULTS",
        )

        app.config["STREAMING"] = True

    return Response(
        stream_with_context(app.config["RESULT_SOURCE"].read_result_data()),
        mimetype="application/octet-stream",
    )


@app.route("/disconnect")
def disconnect():

    source = app.config.get("STREAMING_SOURCE", None)
    source_resutlts = app.config.get("RESULT_SOURCE", None)

    if source is not None:
        source.disconnect()

        del app.config["STREAMING_SOURCE"]
        app.config["STREAMING_SOURCE"] = None

        print("Disconnected from Streaming Source.")

    if source_resutlts is not None:
        source_resutlts.disconnect()

        del app.config["RESULT_SOURCE"]
        app.config["RESULT_SOURCE"] = None

        print("Disconnected from Result Source.")

    app.config["STREAMING"] = False

    return get_config()


if __name__ == "__main__":
    import os

    HOST = os.environ.get("SERVER_HOST", "localhost")
    try:
        PORT = int(os.environ.get("SERVER_PORT", "5555"))
    except ValueError:
        PORT = 5555

    if os.path.exists("./.config.cache"):
        app.config.update(json.load(open("./.config.cache", "r")))

    app.run(HOST, 5555)  # , debug=True)

