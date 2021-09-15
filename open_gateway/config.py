import os

SECRET_KEY = "any secret string"
# Serial BAUD RATE
BAUD_RATE = 460800
# Replace this with the class map
CLASS_MAP = {65534: "Classification Limit Reached", 0: "Unknown"}
# replace this with the dictionary in the model.json file
MODEL_JSON = None
# number of packets to bundle when sending out
CONFIG_SAMPLES_PER_PACKET = 1
# convert incoming data to int16
CONVERT_TO_INT16 = True
# settings to scale incoming data by
SCALING_FACTOR = 1
# path to a libsensiml.so file if this is included the model will be run when live streaming data.
SML_LIBRARY_PATH = os.path.join(
    os.path.dirname(__file__), "knowledgepack", "libsensiml"
)
RUN_SML_MODEL = (
    True if os.path.exists(os.path.join(SML_LIBRARY_PATH, "libsensiml.so")) else False
)
