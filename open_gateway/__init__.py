import os

basedir = os.path.join(os.path.dirname(__file__), "..", "database")


def ensure_folder_exists(name):
    if not os.path.exists(os.path.join(basedir, name)):
        os.mkdir(os.path.join(basedir, name))
