import cv2
import numpy as np
import RPi.GPIO as GPIO
from time import sleep
from picamera2 import Picamera2
from libcamera import controls
import os

#define pins
pin_rcwl = 17
pin_button = 22
pin_flash = 27
pin_confirmation = 18
#relevant helper variables
r_button = 0
r_radar = 0
r_camera = 0
r_flash = 0
r_confirmation = 0
#set GPIO to BCM numbering
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#set up the pushbutton to pin 22 
GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN);   
#set up the FLASH LED to pin 27
GPIO.setup(pin_flash, GPIO.OUT)
#set up the CONFIRMATION LED to pin 18
GPIO.setup(pin_confirmation, GPIO.OUT)

#set up OPENCV stuff
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

#-------------------------------------HELPER FUNCTION (START)-------------
#helper function - LED flashing
def flasher():
    for i in range(5):
        GPIO.output(pin_flash, GPIO.HIGH)
        sleep(0.5)
        GPIO.output(pin_flash, GPIO.LOW)
        sleep(0.5)

def button_callback(channel):
    global r_button
    r_button = 1
    print('Button Pressed')
    GPIO.output(pin_confirmation, GPIO.HIGH)
    sleep(1)
    flasher()
    GPIO.output(pin_confirmation, GPIO.LOW)

#helper function - radar callback
def radar_callback(thepin):
    global r_radar
    if GPIO.input(pin_rcwl):
        r_radar = 1;
    else:
        r_radar = 0;

#setup webcam stuff
def capture_image():
    picam2 = Picamera2()
    os.system("v4l2-ctl --set-ctrl wide_dynamic_range=1 -d /dev/v4l-subdev0")
    print("Setting HDR to ON")
    picam2.start(show_preview=True)
    picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous, "AfSpeed": controls.AfSpeedEnum.Fast})
    picam2.start_and_capture_files("image.png", num_files=3, delay=1)
    picam2.stop_preview()
    picam2.stop()
    print("Setting HDR to OFF")
    os.system("v4l2-ctl --set-ctrl wide_dynamic_range=0 -d /dev/v4l-subdev0")
#-------------------------------------HELPER FUNCTION (END)---------------

#FIND INITIAL CONDITION
index = 0
#Main Loop
GPIO.add_event_detect(pin_button, GPIO.RISING, callback = button_callback, bouncetime=200)
while True:
    #delay of one second
    #call button - physical verification
    sleep(1)
    #camera input - if detection, set r_camera to 1
    capture_image()
    image = cv2.imread('image.png')
    #Resize image for detection
    image = cv2.resize(image, (640,480))
    #Detecting all the regions in the image that has pedestrians
    (regions,_) = hog.detectMultiScale(image, winStride=(4,4), padding=(4,4), scale=1.05)
    for (x,y,w,h) in regions:
        cv2.rectangle(image, (x,y), (x+w,y+h), (0,0,255), 2)
        rects = np.array([x,y,x+w,y+h])
                         
    cv2.imwrite('pedestriantest_output.png', image);
    #if detection
    if len(regions) > 0:
        r_camera = 1
        #activate confirmation LED
        GPIO.output(pin_confirmation, GPIO.HIGH)


        #Option 1 - BYPASS RADAR SENSOR
        flasher()
        GPIO.output(pin_confirmation, GPIO.LOW)
        #Option 2 - USE RADAR SENSOR (BIG GAMBLE)
        #call radar sensor
        #while index < 1:
         #   #until radar + led detect
          #  GPIO.add_event_detect(pin_rcwl, GPIO.BOTH, callback=radar_callback)
           # if (r_radar == 1):
            #    flasher()
             #   index+=1




   
    

