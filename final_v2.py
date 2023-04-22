import cv2
import numpy as np
import RPi.GPIO as GPIO
from time import sleep
from picamera import PiCamera

#define pins
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
GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#set up the FLASH LED to pin 27
GPIO.setup(pin_flash, GPIO.OUT)
#set up the CONFIRMATION LED to pin 18
GPIO.setup(pin_confirmation, GPIO.OUT)

#set up OPENCV stuff
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

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

def capture_and_detect():
    global r_camera
    picam = PiCamera()
    picam.resolution = (640, 480)
    picam.start_preview()
    sleep(2) #warm up time for camera
    for i, filename in enumerate(picam.capture_continuous('image{counter}.png', format='png', use_video_port=True)):
        image = cv2.imread(filename)
        #Detecting all the regions in the image that has pedestrians
        (regions,_) = hog.detectMultiScale(image, winStride=(4,4), padding=(4,4), scale=1.05)
        for (x,y,w,h) in regions:
            cv2.rectangle(image, (x,y), (x+w,y+h), (0,0,255), 2)
            rects = np.array([x,y,x+w,y+h])
        cv2.imwrite(f"pedestriantest_output_{i}.png", image)
        #if detection
        if len(regions) > 0:
            r_camera = 1
            #activate confirmation LED
            GPIO.output(pin_confirmation, GPIO.HIGH)
            flasher()
            GPIO.output(pin_confirmation, GPIO.LOW)
        sleep(2) # wait for next image capture

#FIND INITIAL CONDITION
index = 0
#Main Loop
GPIO.add_event_detect(pin_button, GPIO.RISING, callback=button_callback, bouncetime=200)
while True:
    #delay of one second
    #call button - physical verification
    #camera input - if detection, set r_camera to 1
    capture_and_detect()
    if r_button == 1 or r_camera == 1:
        GPIO.output(pin_confirmation, GPIO.HIGH)
        flasher()
        GPIO.output(pin_confirmation, GPIO.LOW)
        r_button = 0
        r_camera = 0
