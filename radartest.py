#from gpiozero import DigitalInputDevice
import RPi.GPIO as GPIO
from time import sleep

pin = 17

#radar = DigitalInputDevice(17, pull_up=False, bounce_time=2.0) 

#def detector():
#    print("Motion Detected")
#while True:
#    radar.when_activated = detector
#    sleep(1)

GPIO.setwarnings(False);
GPIO.setmode(GPIO.BCM)

def gpiocallback(thepin):
    
    if GPIO.input(pin):
        print('true')
    else:
        print('false')

GPIO.setup(pin, GPIO.IN)
GPIO.add_event_detect(pin, GPIO.BOTH, callback=gpiocallback)

while True:
    print('sleeping')
    time.sleep(2)