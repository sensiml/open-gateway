import os
import subprocess
import sys
import re


def get_video_source(camera_index):

    if camera_index == -1:
        from video_sources.screen_capture import ScreenCatpure

        return ScreenCatpure(camera_index)

    else:
        from video_sources.webcam import WebCam

        return WebCam(camera_index)


def list_cameras_darwin():
    os.system("ioreg | grep -i cam | grep -i IOUSBHost > cameras.txt")
    cameras = []

    with open("cameras.txt", "r") as fid:
        counter = 0
        for line in fid.readlines():
            cameras.append(
                {
                    "name": line.split("+-o")[-1].lstrip().split("<class")[0],
                    "index": counter,
                }
            )

            counter += 1

    return cameras


def list_cameras_linux():

    # cmd = """v4l2-ctl --list-devices | awk '{split($0,a,"-"); gsub(/[):]/,"",a[3]); getline; name=substr($0,2); print a[3] "-" name; getline}'"""
    # cmd = "v4l2-ctl --list-devices > cameras.txt"
    cmd = "ls /dev/video* > cameras.txt"
    os.system(cmd)
    cameras = []

    with open("cameras.txt", "r") as fid:
        counter = 0
        for line in fid.readlines():
            line = line.rstrip().lstrip()
            cameras.append({"name": line, "index": counter})
            counter += 1

    return cameras


def list_cameras_windows():

    """Get-PnpDevice -Status OK -FriendlyName *webcam* -Class camera,image > cameras.txt"""

    p = subprocess.Popen(
        [
            "powershell.exe",
            "Get-PnpDevice",
            "-Status",
            "OK",
            "-FriendlyName",
            "*webcam*",
            "-Class",
            "camera,image",
        ],
        stdout=subprocess.PIPE,
        text=True,
    )

    cameras = []
    counter = 0
    for line in p.stdout.readlines():
        line = re.sub("\s\s+", "\t", line).split("\t")
        if len(line) > 1 and line[1] in ["Camera", "Image"]:
            cameras.append({"name": line[2], "index": counter})
            counter += 1

    return cameras


def get_video_source_list():

    video_sources = [{"index": -1, "name": "Screen Capture"}]

    if sys.platform == "darwin":
        camera_list = list_cameras_darwin()

    if sys.platform == "win32":
        camera_list = list_cameras_windows()

    if sys.platform == "linux":
        camera_list = list_cameras_linux()

    video_sources.extend(camera_list)

    return video_sources


def get_video_source_name(camera_index):
    video_source_list = get_video_source_list()
    for video_source in video_source_list:
        if video_source["index"] == camera_index:
            return video_source["name"]

    return None


if __name__ == "__main__":

    print(get_video_source_list())

    """
    import cv2
    # checks the first 10 indexes.
    index = 0
    arr = []
    i = 5
    while i > 0:
        cap = cv2.VideoCapture(index)
        r = cap.read()
        if cap.read()[0]:
            arr.append(index)
            cap.release()
        index += 1
        i -= 1
    return arr
    """
