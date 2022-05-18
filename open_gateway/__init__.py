import os

from appdirs import *

appname = "Open Gateway"
appauthor = "SensiML"
__version__ = "2022.5.18.0"
basedir = user_data_dir(appname, appauthor)
print("captured data stored in {basedir}".format(basedir=basedir))


config = {
    "SECRET_KEY": "any secret string",
    "BAUD_RATE": 460800,
    "DATA_TYPE": "int16",
    "CLASS_MAP": {65534: "Classification Limit Reached", 0: "Unknown"},
    "MODEL_JSON": None,
    "CONFIG_SAMPLES_PER_PACKET": 1,
    "CONVERT_TO_INT16": True,
    "SCALING_FACTOR": 1,
}


def ensure_folder_exists(name):
    if not os.path.exists(os.path.join(basedir, name)):
        os.mkdir(os.path.join(basedir, name))
