import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)	#set GPIO to BCM numbering
#GPIO.setwarnings(False)	#disable GPIO warnings
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def button_callback(channel):
    print("Button Pressed")

GPIO.add_event_detect(27, GPIO.RISING, callback=button_callback, bouncetime=200)

#Main Loop
try:
    while True:
        sleep(0.1)
        
except KeyboardInterrupt:
    GPIO.cleanup()
