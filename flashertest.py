import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)	#set GPIO to BCM numbering
GPIO.setwarnings(False)	#disable GPIO warnings
GPIO.setup(27, GPIO.OUT)

while True:
    GPIO.output(27, GPIO.HIGH)
    sleep(1)
    GPIO.output(27, GPIO.LOW)
    sleep(1)