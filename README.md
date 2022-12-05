# rpi-cam
Simple raspberry pi camera capture with some handling of captured videos

```bash
python -m venv /home/pi/rpi-camv
source /home/pi/rpi-camv/bin/activate
pip install ephem
```

Clone repo:

```bash
git clone https://github.com/alexey-pronkin/rpi-cam.git
```

Change variables inside rpi-cam.py to your values:

VIDEOS_PATH = '/home/pi/Desktop/videos/'
MAX_FOLDER_SIZE = 60 * 1_000_000
VIDEOS_LENGHT = 60 * 60 * 8 # in seconds
USE_NIGHT_MODE = True
LAT = 55.494120 # Camera latitude
LON = 38.661637 # Camera longitude

Start recording

```bash
cd rpi-cam
python rpi-cam/rpi-cam.py
```