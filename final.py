import cv2
import numpy as np
import RPi.GPIO as GPIO
from time import sleep

#define pins
pin_rcwl = 17
pin_button = 22
pin_flash = 27
pin_confirmation = 18
#set GPIO to BCM numbering
GPIO.setmode(GPIO.BCM) 
#set up the pushbutton to pin 22 
GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN);   
#set up the FLASH LED to pin 27
GPIO.setup(pin_flash, GPIO.OUT)
#set up the CONFIRMATION LED to pin 18


