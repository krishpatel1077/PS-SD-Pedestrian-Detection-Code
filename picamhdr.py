import cv2
import imutils
import numpy as np
from picamera2 import Picamera2
from libcamera import controls
import os
picam2 = Picamera2()
os.system("v4l2-ctl --set-ctrl wide_dynamic_range=1 -d /dev/v4l-subdev0")
print("Setting HDR to ON")
picam2.start(show_preview=True)
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous, "AfSpeed": controls.AfSpeedEnum.Fast})
picam2.start_and_capture_files("HDRfastfocus{:d}.jpg", num_files=3, delay=1)
picam2.stop_preview()
picam2.stop()
print("Setting HDR to OFF")
os.system("v4l2-ctl --set-ctrl wide_dynamic_range=0 -d /dev/v4l-subdev0")



