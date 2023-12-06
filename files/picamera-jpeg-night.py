#!/usr/bin/python3

# Start camera with fixed exposure and gain.

import time

from picamera2 import Picamera2, Preview

picam2 = Picamera2()
#picam2.start_preview(Preview.QTGL)
controls = {"ExposureTime": 10000, "AnalogueGain": 1.0}
preview_config = picam2.create_preview_configuration(controls=controls, main={"size": (1920, 1080)})
picam2.configure(preview_config)

picam2.start()
time.sleep(5)

metadata = picam2.capture_file("photo-night.jpg")
print(metadata)

picam2.close()
