import os
from datetime import datetime
from pathlib import Path
from time import sleep

import ephem
from picamera import PiCamera

VIDEOS_PATH = '/home/pi/Desktop/videos/'
MAX_FOLDER_SIZE = 60 * 1_000_000
VIDEOS_LENGHT = 60 * 60 * 8 # in seconds
USE_NIGHT_MODE = True
LAT = 55.494120 # Camera latitude
LON = 38.661637 # Camera longitude

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

if __name__ == "__main__":
    os.makedirs(VIDEOS_PATH, exist_ok=True)
    while True:
        if get_size(path=VIDEOS_PATH) > MAX_FOLDER_SIZE:
            handle_file(path=VIDEOS_PATH)
        n = datetime.now()

        if USE_NIGHT_MODE:
            observer = ephem.Observer()
            sun = ephem.Sun()
            observer.lat = LAT
            observer.lon = LON
            observer.date = n
            rise_time = obs.next_rising(sun)
            set_time = obs.next_setting(sun)
            if (n > set_time) and (n < rise_time):
                ## Night mode from tutorial:
                # Force sensor mode 3 (the long exposure mode), set
                # the framerate to 5 fps, the shutter speed to 6s,
                # and ISO to 800 (for maximum gain)
                camera = PiCamera(
                    framerate=5,
                    sensor_mode=3)
                camera.shutter_speed = 6000000
                camera.iso = 800
                camera.exposure_mode = 'night'
            else:
                camera = PiCamera()
        else:
            camera = PiCamera()
        
        camera.start_preview()
        camera.annotate_background = picamera.Color('black')
        camera.annotate_text = n.strftime('%Y-%m-%d %H:%M:%S')
        camera.start_recording(VIDEOS_PATH+f'{n.isoformat(timespec="seconds")}.h264')
        sleep(VIDEOS_LENGHT)
        camera.stop_recording()
        camera.stop_preview()
