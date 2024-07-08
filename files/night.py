#!/usr/bin/python3

from picamera2 import Picamera2
from datetime import datetime

picam2 = Picamera2()
config = picam2.create_still_configuration(buffer_count=6)
picam2.configure(config)
picam2.set_controls({"ExposureTime": 80000000, "AnalogueGain": 8, "ColourGains": (2, 1.81)})
picam2.start()

#while True:
picam2.capture_file(datetime.now().strftime("photo-night.jpg"))
