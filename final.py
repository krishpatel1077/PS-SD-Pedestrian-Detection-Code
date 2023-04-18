import cv2
import numpy as np
import RPi.GPIO as GPIO
from time import sleep

#define pins
pin_rcwl = 17
pin_button = 22
pin_flash = 27
pin_confirmation = 18
#relevant helper variables
r_button, r_radar, r_camera, r_flash, r_confirmation, r_button = 0
#set GPIO to BCM numbering
GPIO.setmode(GPIO.BCM) 
#set up the pushbutton to pin 22 
GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN);   
#set up the FLASH LED to pin 27
GPIO.setup(pin_flash, GPIO.OUT)
#set up the CONFIRMATION LED to pin 18
GPIO.setup(pin_confirmation, GPIO.OUTPUT)

#set up OPENCV stuff
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

#-------------------------------------HELPER FUNCTION (START)-------------
#helper function - LED flashing
def flasher():
    GPIO.output(pin_flash, GPIO.HIGH)
    sleep(1)
    GPIO.output(pin_flash, GPIO.LOW)
    sleep(1)
    GPIO.output(pin_flash, GPIO.HIGH)
    sleep(1)
    GPIO.output(pin_flash, GPIO.LOW)
    sleep(1)
    GPIO.output(pin_flash, GPIO.HIGH)
    sleep(1)
    GPIO.output(pin_flash, GPIO.LOW)
    sleep(1)
    GPIO.output(pin_flash, GPIO.HIGH)
    sleep(1)
    GPIO.output(pin_flash, GPIO.LOW)
    sleep(1)
    GPIO.output(pin_flash, GPIO.HIGH)
    sleep(1)
    GPIO.output(pin_flash, GPIO.LOW)
    sleep(1)

#helper function - confirmation LED
# def confirmer():
#     GPIO.output(pin_flash, GPIO.HIGH)
#     sleep(1)
#     GPIO.output(pin_flash, GPIO.LOW)
#     sleep(1)
#helper function - button callback
def button_callback(channel):
    r_button = 1;
    GPIO.output(pin_confirmation, GPIO.HIGH)

#helper function - radar callback
def radar_callback(thepin):
    if GPIO.input(pin_rcwl):
        r_radar = 1;
    else:
        r_radar = 0;

#setup webcam stuff
def capture_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite('image.png', frame)
    cap.release()
#setup rpicamera stuff
#TBD - TOMORROW IF SHIPPING ARRIVES
#-------------------------------------HELPER FUNCTION (END)---------------

#FIND INITIAL CONDITION
index = 0
#Main Loop
while True:
    #delay of one second
    #call button - physical verification
    GPIO.add_event_detect(pin_button, GPIO.RISING, callback = button_callback, bouncetime=200)
    sleep(1)
    #camera input - if detection, set r_camera to 1
    capture_image()
    image = cv2.imread('image.png')
    #Resize image for detection
    image = cv2.resize(image, (640,480))
    #Detecting all the regions in the image that has pedestrians
    (regions,_) = hog.detectMultiScale(image, winStride=(4,4), padding=(4,4), scale=1.05)
    #if detection
    if len(regions) > 0:
        r_camera = 1
        #activate confirmation LED
        GPIO.output(pin_confirmation, GPIO.HIGH)


        #Option 1 - BYPASS RADAR SENSOR
        #GPIO.output(flasher)

        #Option 2 - USE RADAR SENSOR (BIG GAMBLE)
        #call radar sensor
        while index < 1:
            #until radar + led detect
            GPIO.add_event_detect(pin_rcwl, GPIO.BOTH, callback=radar_callback)
            if (r_radar == 1):
                flasher()
                index+=1




   
    

