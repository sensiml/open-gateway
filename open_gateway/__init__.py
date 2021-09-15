import os

basedir = os.path.join(os.path.dirname(__file__), "..", "database")


config = {
    "SECRET_KEY": "any secret string",
    "BAUD_RATE": "460800",
    "CLASS_MAP": {65534: "Classification Limit Reached", 0: "Unknown"},
    "MODEL_JSON": None,
    "CONFIG_SAMPLES_PER_PACKET": 1,
    "CONVERT_TO_INT16": True,
    "SCALING_FACTOR": 1,
    "SML_LIBRARY_PATH": os.path.join(basedir, "knowledgepack", "libsensiml"),
}


def ensure_folder_exists(name):
    if not os.path.exists(os.path.join(basedir, name)):
        os.mkdir(os.path.join(basedir, name))
