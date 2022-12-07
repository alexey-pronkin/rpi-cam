import os
from datetime import datetime
from pathlib import Path
from time import sleep

import ephem
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder, Quality

VIDEOS_PATH = '/home/pi/Desktop/videos/'
MAX_FOLDER_SIZE = 60 * 1_000_000
VIDEOS_LENGHT = 60 * 60 * 8 # in seconds, divided by 3600
USE_NIGHT_MODE = True
LAT = 55.494120 # Camera latitude
LON = 38.661637 # Camera longitude
DEBUG = False

def handle_file(path):
    filenames = os.listdir(path=path)
    filenames.sort()
    try:
        os.remove(path=path+filenames[0])
    except OSError:
        print("File already deleted")

def get_size(path):
    folder_size = 0  
    for p in os.scandir(path=path):
        folder_size += os.stat(p).st_size
    return folder_size

def get_day_or_night(n):
    observer = ephem.Observer()
    sun = ephem.Sun()
    observer.lat = LAT
    observer.lon = LON
    observer.date = n
    rise_time = observer.next_rising(sun)
    set_time = observer.next_setting(sun)
    if (n > set_time.datetime()) and (n < rise_time.datetime()):
        return "night"
    else:
        return "day"
def night_mode():
    ## Night mode from tutorial: https://picamera.readthedocs.io/en/release-1.13/fov.html?highlight=night#sensor-gain
    # Force sensor mode 3 (the long exposure mode), set
    # the framerate to 5 fps, the shutter speed to 6s,
    # and ISO to 800 (for maximum gain)
    camera = Picamera2()
    if DEBUG > 0:
        print(camera.sensor_modes)
    config = camera.create_preview_configuration({'fps': 10})
    # raw=camera.sensor_modes[2]
    camera.configure(config)
    camera.set_controls({"ExposureTime": 250, "AnalogueGain": 8.0})
    return camera

def day_mode(): 
    camera = Picamera2()
    camera.configure(camera.create_video_configuration())
    return camera

def time_logic(n):
    if get_day_or_night(n) == "day":
        camera = day_mode()
        mode = "day"
    elif get_day_or_night(n) == "night":
        camera = night_mode()
        mode = "night"
    else:
        print("BUG, there is only day and night modes")
    return camera, mode

if __name__ == "__main__":
    os.makedirs(VIDEOS_PATH, exist_ok=True)
    encoder = H264Encoder()
    while True:
        if get_size(path=VIDEOS_PATH) > MAX_FOLDER_SIZE:
            handle_file(path=VIDEOS_PATH)
        n = datetime.now()
        if USE_NIGHT_MODE:
            camera, mode = time_logic(n=n)
        else:
            camera = day_mode()
        if DEBUG > 0:
            print(camera.sensor_modes)
        camera.start_preview(Preview.QTGL)
        # camera.annotate_background = picamera.Color('black')
        # camera.annotate_text = n.strftime('%Y-%m-%d %H:%M:%S')
        camera.start_recording(encoder,VIDEOS_PATH+f'{n.isoformat(timespec="seconds")}.h264', Quality.VERY_HIGH)
        for t in range(sleep(VIDEOS_LENGHT) // 3600):
            n = datetime.now()
            if USE_NIGHT_MODE:
                if get_day_or_night(n) != mode:
                    camera.stop_recording()
                    camera.stop_preview()
                    continue
            sleep(3600)
        camera.stop_recording()
        camera.stop_preview()
