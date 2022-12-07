# rpi-cam
Simple raspberry pi camera capture with auto deleting of old captured videos. Also night/day modes in alpha test.

For now, a picamera is hard to install into some virtual environment, so it's better to install all into the system python:
```bash
sudo apt install -y python3-pyqt5 python3-opengl
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3-picamera2
pip install ephem
```

Users of Raspberry Pi 3 or earlier devices will need to enable *Glamor* in order for this example script using X Windows to work. To do this, run `sudo raspi-config` in a command window, choose Advanced Options and then
enable *Glamor graphic acceleration*. Finally reboot your device.

Clone repo:

```bash
git clone https://github.com/alexey-pronkin/rpi-cam.git
```

Change variables inside rpi-cam.py to your values:
```python
VIDEOS_PATH = '/home/pi/Desktop/videos/'
MAX_FOLDER_SIZE = 60 * 1_000_000
VIDEOS_LENGHT = 60 * 60 * 8 # in seconds, should be divisible by 3600
USE_NIGHT_MODE = True
LAT = 55.494120 # Camera latitude
LON = 38.661637 # Camera longitude
```

Start recording

```bash
cd rpi-cam
python rpi-cam/rpi-cam.py
```