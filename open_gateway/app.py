import os
import json
import sys
import shutil
from json import dumps
import asyncio
import nest_asyncio
import time
from threading import Timer
import webbrowser
import getopt

nest_asyncio.apply()

from flask import (
    Flask,
    Response,
    stream_with_context,
    request,
    jsonify,
    make_response,
    send_from_directory,
)
from flask_cors import CORS
from open_gateway.forms import (
    DeviceConfigureForm,
    DeviceScanForm,
    DeviceRecordForm,
    CameraForm,
)
from open_gateway.sources import get_source
from open_gateway.errors import errors
from open_gateway.video_sources import get_video_source, get_video_source_list
import zipfile
from open_gateway import basedir, ensure_folder_exists


app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), "..", "webui", "build"),
    static_url_path="/",
)
# app.register_blueprint(errors)
CORS(app, resources={r"/*": {"origins": "*"}})
loop = asyncio.get_event_loop()
app.config.from_object("open_gateway.config")


## Internal Config Settings
app.config["CONFIG_SAMPLE_RATE"] = None
app.config["SOURCE_SAMPLES_PER_PACKET"] = None
app.config["DATA_TYPE"] = "int16"
app.config["DATA_SOURCE"] = None
app.config["CONFIG_COLUMNS"] = []
app.config["DEVICE_ID"] = None
app.config["DEVICE_SOURCE"] = None
app.config["MODE"] = ""
app.config["VIDEO_SOURCE"] = None
app.config["LOOP"] = loop


# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


def cache_config(config):
    tmp = {
        "CONFIG_SAMPLE_RATE": app.config["CONFIG_SAMPLE_RATE"],
        "DATA_SOURCE": app.config["DATA_SOURCE"],
        "CONFIG_COLUMNS": app.config["CONFIG_COLUMNS"],
        "DEVICE_ID": app.config["DEVICE_ID"],
        "MODE": app.config["MODE"],
        "SOURCE_SAMPLES_PER_PACKET": app.config["SOURCE_SAMPLES_PER_PACKET"],
        "DATA_TYPE": app.config["DATA_TYPE"],
    }
    json.dump(tmp, open(os.path.join(basedir, ".config.cache"), "w"))


@app.route("/")
def main():
    return app.send_static_file("index.html")


def get_device_id():
    return app.config["DEVICE_ID"]


def get_samples_per_packet():
    if app.config["DEVICE_SOURCE"]:
        return app.config["DEVICE_SOURCE"].packet_buffer_size

    return 1


def get_streaming():
    if app.config["DEVICE_SOURCE"]:
        return app.config["DEVICE_SOURCE"].is_streaming()

    return False


def get_recording():
    if app.config["DEVICE_SOURCE"]:
        return app.config["DEVICE_SOURCE"].is_recording()

    return False


def parse_current_config():

    ret = {}
    ret["sample_rate"] = app.config["CONFIG_SAMPLE_RATE"]
    ret["column_location"] = dict()
    ret["samples_per_packet"] = get_samples_per_packet()
    ret["source_samples_per_packet"] = app.config["SOURCE_SAMPLES_PER_PACKET"]
    ret["source"] = app.config["DATA_SOURCE"]
    ret["device_id"] = get_device_id()
    ret["streaming"] = get_streaming()
    ret["baud_rate"] = app.config["BAUD_RATE"]
    ret["mode"] = app.config["MODE"].lower()
    ret["recording"] = get_recording()
    ret["data_type"] = (
        app.config["DATA_TYPE"] if not app.config["CONVERT_TO_INT16"] else "int16"
    )

    if app.config["CONFIG_COLUMNS"]:
        ret["column_location"] = app.config["CONFIG_COLUMNS"]
    else:
        ret["column_location"] = {}

    if app.config["VIDEO_SOURCE"]:
        ret.update(app.config["VIDEO_SOURCE"].info())
    else:
        ret.update(
            {
                "camera_on": False,
                "camera_record": False,
                "camera_index": None,
                "camrea_name": None,
            }
        )

    return ret


def get_config():

    ret = parse_current_config()

    return Response(dumps(ret), mimetype="application/json")


@app.route("/scan-devices", methods=["POST"])
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

    if app.config.get("DEVICE_SOURCE", None) is None:

        app.config["DEVICE_SOURCE"] = get_source(
            app.config,
            device_id=get_device_id(),
            data_source=app.config["DATA_SOURCE"],
            source_type=app.config["MODE"],
        )

        app.config["DEVICE_SOURCE"].update_config(app.config)

        app.config["DEVICE_SOURCE"].connect()

    return get_config()


@app.route("/disconnect")
def disconnect():

    if app.config.get("DEVICE_SOURCE", None) is not None:

        app.config["DEVICE_SOURCE"].disconnect()
        app.config["DEVICE_SOURCE"] = None

        print("Disconnected from device.")

    return get_config()


@app.route("/config-device", methods=["GET", "POST"])
@app.route("/config", methods=["GET", "POST"])
def config():
    form = DeviceConfigureForm()

    if request.method == "POST":
        disconnect()

        source = get_source(
            app.config,
            data_source=form.data["source"].upper(),
            source_type=form.data["mode"].upper(),
            device_id=form.data["device_id"],
        )

        source.read_config()

        print("App: Configuring source reader")
        source.set_app_config(app.config)

        print("App: Connecting to device")
        source.connect()

        app.config["MODE"] = form.data["mode"].upper()

        cache_config(app.config)

        app.config["DEVICE_SOURCE"] = source

    ret = parse_current_config()

    return Response(dumps(ret), mimetype="application/json")


@app.route("/results")
@app.route("/stream")
def stream():

    if app.config.get("DEVICE_SOURCE", None) is None:
        return make_response(
            jsonify(detail="Must Connect to device before starting stream"), 400
        )

    return Response(
        stream_with_context(app.config["DEVICE_SOURCE"].read_data()),
        mimetype="application/octet-stream",
    )


@app.route("/scan-video", methods=["GET"])
def scan_video():
    """ "

    returns a list of video sources available

    """

    video_source_list = get_video_source_list()

    return Response(
        dumps({"video_sources": video_source_list}), mimetype="application/json"
    )


@app.route("/config-video", methods=["GET", "POST"])
def config_video():
    """Start/Stop Video Source

    params:
        event_type (str): camera-on - turns the camera on
                          camera-off - turns the camera off

        camera_index (int): index of the video source to use

    """
    form = CameraForm()

    event_type = form.data["event_type"]
    camera_index = form.data["camera_index"]

    if request.method == "POST":

        if event_type == "camera-on":

            if app.config["VIDEO_SOURCE"]:
                return make_response(jsonify(detail="Camera already on"), 200)

            app.config["VIDEO_SOURCE"] = get_video_source(camera_index)
            app.config["VIDEO_SOURCE"].start()

            return jsonify(detail="Camera Started")

        if event_type == "camera-off":

            if app.config["VIDEO_SOURCE"] is None:
                return make_response(jsonify(detail="Camera is already off"), 200)

            print("Deleting video camera object")
            app.config["VIDEO_SOURCE"].off()
            del app.config["VIDEO_SOURCE"]
            app.config["VIDEO_SOURCE"] = None

            return jsonify(detail="Camera turned off")

        else:
            return make_response(
                jsonify(detail="Invalid Event Type: {}".format(event_type)), 400
            )

    if request.method == "GET":

        resp = {
            "camera_on": False,
            "camera_record": False,
            "camera_index": None,
            "camera_name": None,
        }

        if app.config["VIDEO_SOURCE"]:
            resp = app.config["VIDEO_SOURCE"].info()

        return Response(dumps(resp), mimetype="application/json")


@app.route("/stream-video", methods=["GET"])
def stream_video():
    """

    Access the stream of the video source data

    """

    if app.config["VIDEO_SOURCE"] is None:
        return make_response(jsonify(detail="Must start camera before streaming"), 400)

    return Response(
        app.config["VIDEO_SOURCE"].generate(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


@app.route("/record-video", methods=["POST"])
def record_video():
    """Record Video Source

    params:
        event_type (str): record-start - starts saving to the filename
                          record-stop - stops recording
        filename (str): name of file to record too

    """

    form = DeviceRecordForm()

    filename = form.data["filename"]
    event_type = form.data["event_type"]

    if app.config["VIDEO_SOURCE"] is None:
        return make_response(
            jsonify(
                detail="Video source not created, you must start camera before recording."
            ),
            400,
        )

    if event_type == "record-stop":

        if app.config["VIDEO_SOURCE"].is_recording():
            app.config["VIDEO_SOURCE"].record_stop()

            return jsonify(detail="Video stopped recording")

        return make_response(jsonify(detail="Video is not recording"), 400)

    if event_type == "record-start":

        if filename is None:
            return make_response(
                jsonify(detail="Must pass filename to start recording"), 400
            )

        if app.config["VIDEO_SOURCE"].is_recording():
            return make_response(
                jsonify(
                    detail="Already recording video source. Only one video stream at a time."
                ),
                400,
            )

        app.config["VIDEO_SOURCE"].record_start(filename)

        return jsonify(detail="Video recording started")

    return make_response(
        jsonify(detail="Not a supported Event Type {}".format(event_type)), 400
    )


@app.route("/record-device", methods=["POST"])
def record_device():
    """Record Sensor Data if available

    params:
        event_type (str): record-start - starts saving to the filename
                          record-stop - stops recording
        filename (str): name of file to record too

    """

    form = DeviceRecordForm()

    filename = form.data["filename"]
    event_type = form.data["event_type"]

    if app.config["DEVICE_SOURCE"] is None:
        return make_response(
            jsonify(
                detail="Must connect to data source before starting/stopping to record!"
            ),
            400,
        )

    if event_type == "record-start":

        if filename is None:
            return make_response(
                jsonify(detail="Must pass filename to start recording!"), 400
            )

        if app.config["DEVICE_SOURCE"].is_recording():
            return make_response(jsonify(detail="Already Recording Device"), 400)

        app.config["DEVICE_SOURCE"].record_start(filename)

        return jsonify(detail="Recording Started!")

    if event_type == "record-stop":

        if app.config["DEVICE_SOURCE"].is_recording():
            app.config["DEVICE_SOURCE"].record_stop(filename)

            return jsonify(detail="Video stopped recording")

        return make_response(jsonify(detail="Video was not recording!"), 400)

    return make_response(
        jsonify(detail="Not a supported Event Type {}".format(event_type)), 400
    )


@app.route("/record", methods=["POST"])
def record():
    """Record Sensor Data and Video if available

    params:
        event_type (str): record-start - starts saving to the filename
                          record-stop - stops recording
        filename (str): name of file to record too

    """

    form = DeviceRecordForm()

    filename = form.data["filename"]
    event_type = form.data["event_type"]

    if event_type == "record-start":

        if app.config["VIDEO_SOURCE"] is None:
            return make_response(
                jsonify(detail="Must start webcam before starting to record!"), 400
            )

        if app.config["DEVICE_SOURCE"] is None:
            return make_response(
                jsonify(
                    detail="Must connect to data source before starting to record!"
                ),
                400,
            )

        if filename is None:
            return make_response(
                jsonify(detail="Must pass filename to start recording!"), 400
            )

        if app.config["VIDEO_SOURCE"].is_recording():
            return make_response(jsonify(detail="Already Recording Video"), 400)

        if app.config["DEVICE_SOURCE"].is_recording():
            return make_response(jsonify(detail="Already Recording Device"), 400)

        app.config["DEVICE_SOURCE"].record_start(filename)
        app.config["VIDEO_SOURCE"].record_start(filename)

        return jsonify(detail="Recording Started!")

    if event_type == "record-stop":

        was_recording = False

        if app.config["VIDEO_SOURCE"] and app.config["VIDEO_SOURCE"].is_recording():
            app.config["VIDEO_SOURCE"].record_stop()
            was_recording = True

        if app.config["DEVICE_SOURCE"] and app.config["DEVICE_SOURCE"].is_recording():
            app.config["DEVICE_SOURCE"].record_stop()
            was_recording = True

        if was_recording:
            return jsonify(detail="recording ended.")

        return make_response(jsonify(detail="Gateway was not recording."), 400)

    return make_response(
        jsonify(detail="Not a supported Event Type {}".format(event_type)), 400
    )


def get_file_dcli(filename):

    video_path = filename[:-4] + ".mp4"
    file_path = filename
    return {
        "file_name": file_path,
        "metadata": [],
        "sessions": [],
        "videos": [{"video_path": video_path}],
    }


@app.route("/download/<path:filename>", methods=["GET", "POST"])
def download_filename(filename):
    # todo needs to handle multiple downloads

    ensure_folder_exists("cache")

    dcli = []

    with zipfile.ZipFile(
        os.path.join(basedir, "cache", "{}.zip".format(filename)), "w"
    ) as zfile:
        datafile_path = os.path.join(basedir, "data", filename + ".csv")
        video_path = os.path.join(basedir, "video", filename + ".mp4")

        dcli.append(get_file_dcli(filename + ".csv"))

        if os.path.exists(datafile_path):
            zfile.write(datafile_path, filename + ".csv")

        if os.path.exists(video_path):
            zfile.write(video_path, filename + ".mp4")

        json.dump(dcli, open(os.path.join(basedir, "{}.dcli".format(filename)), "w"))
        zfile.write(os.path.join(basedir, "{}.dcli".format(filename)))

    return send_from_directory(
        directory=os.path.join(basedir, "cache"),
        # path="{}.zip".format(filename),
        filename="{}.zip".format(filename),
        mimetype="application/zip",
        as_attachment=True,
    )


@app.route("/download", methods=["GET", "POST"])
def download():
    # todo needs to handle multiple downloads

    ensure_folder_exists("cache")

    dcli = []

    with zipfile.ZipFile(os.path.join(basedir, "cache", "data.zip"), "w") as zfile:

        for filename in os.listdir(os.path.join(basedir, "data")):
            datafile_path = os.path.join(basedir, "data", filename)
            zfile.write(datafile_path, filename)
            dcli.append(get_file_dcli(filename))

        for filename in os.listdir(os.path.join(basedir, "video")):
            datafile_path = os.path.join(basedir, "video", filename)
            zfile.write(datafile_path, filename)

        json.dump(dcli, open(os.path.join(basedir, "data.dcli"), "w"))
        zfile.write(os.path.join(basedir, "data.dcli"))

    return send_from_directory(
        directory=os.path.join(basedir, "cache"),
        # path="data.zip",
        filename="data.zip",
        mimetype="application/zip",
        as_attachment=True,
    )


@app.route("/delete-cache", methods=["GET", "POST"])
def delete_cache():
    # todo needs to handle multiple downloads

    for cache_dir in ["cache", "data", "video"]:
        if os.path.exists(os.path.join(basedir, cache_dir)):
            shutil.rmtree(os.path.join(basedir, cache_dir))

    return jsonify(detail="cache deleted.")


def main():

    options_string = """
python app.py -u <host> -p <port> -s <path-to-libsensiml.so-folder> -m <path-to-model-json-file> -c <True/False> -f <scaling-factor> 

-u --host (str) : select the host address for the gateway to launch on
-p --port (int) : select the port address for the gateway to launch on
-s --sml_library_path (str): set a path a knowledgepack libsensiml.so in order to run the model against the live streaming gateway data
-m --model_json_path (str): set to the path of them model.json from the knowledgepack and this will use the classmap described in the model json file 
-c --convert_to_int16 (bool): set to True to convert incoming data from float to int16 values
-f --scaling_factor (int): number to multiple incoming data by prior to converting to int16 from float

"""
    HOST = os.environ.get("SERVER_HOST", "localhost")
    PORT = 5555

    ensure_folder_exists(basedir)

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hu:p:s:c:f:m:",
            [
                "help",
                "host",
                "port",
                "sml_library_path",
                "convert_to_in16",
                "scaling_factor",
            ],
        )
    except getopt.GetoptError:
        print("Invalid nvalid opt selection!")
        print(options_string)
        sys.exit()

    for opt, arg in opts:
        print(opt, arg)
        if opt in ("-h", "--help"):
            print(options_string)
            sys.exit()
        if opt in ("-u", "--host"):
            HOST = arg
        elif opt in ("-p", "--port"):
            print(opt)
            PORT = int(arg)
        elif opt in ("-s", "--sml_library_path"):
            app.config["SML_LIBRARY_PATH"] = arg
            if os.name == "nt":
                app.config["RUN_SML_MODEL"] = (
                    True
                    if os.path.exists(os.path.join(arg, "libsensiml.dll"))
                    else False
                )
            else:
                app.config["RUN_SML_MODEL"] = (
                    True
                    if os.path.exists(os.path.join(arg, "libsensiml.so"))
                    else False
                )
            if not app.config["RUN_SML_MODEL"]:
                print("libsensiml not found in {}".format(arg))
                raise Exception("libsensiml.so not found in {}".format(arg))
        elif opt in ("-m", "--model_json_path"):
            if os.path.exists(arg):
                app.config["MODEL_JSON"] = json.load(open(arg))
            else:
                print("Model json file was not found!")
        elif opt in ("-c", "--convert_to_int16"):
            app.config["CONVERT_TO_INT16"] = arg
        elif opt in ("-f", "--scaling_factor"):
            print("setting scaling factor", arg)
            app.config["SCALING_FACTOR"] = int(arg)

    if os.path.exists(os.path.join(basedir, ".config.cache")):
        app.config.update(json.load(open(os.path.join(basedir, ".config.cache"), "r")))

    # print(app.config)

    try:
        Timer(2, webbrowser.open_new("http://" + HOST + ":" + str(PORT)))
        app.run(HOST, PORT)
    except KeyboardInterrupt:
        print("Keyboard Interupt Detected. Shutting down server!")
    finally:
        print("Disconnecting from all devices!")
        if app.config["DEVICE_SOURCE"] is not None:
            app.config["DEVICE_SOURCE"].disconnect()
            for i in range(5):
                print(".")
                time.sleep(1)
        print("Shutting down server!")
        sys.exit()


if __name__ == "__main__":
    main()