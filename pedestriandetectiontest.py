import cv2
import imutils
import numpy as np

#pushbutton stuff
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
#change pin to actually work
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
# Set pin 10 to be an input pin and set initial value to be pulled low (off)


#RCWL-0516 + RPICAMERA STUFF
from gpiozero import DigitalInputDevice
import datetime
#from picamera import PiCamera
from signal import pause 

#set up doppler radar sensor
radar = DigitalInputDevice(17, pull_up=False, bounce_time=2.0)

#def detector():






#HOGDescriptptor - structure identifying feature used by openCV
#For purpose of this code, using default people detection pkg
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

#read test image
image = cv2.imread('pedestrian-header3.png')

#COMMENTED PORTION FROM LINES 13 - 27 SHOW WEBCAM INPUT WITH PEDESTRIAN DETECTION
#CAN NOT BE TESTED IN FULL UNTIL RPI CAM IS AVAILABLE

    #cap = cv2.VideoCapture(0)
    #ret, frame = cap.read()
    #if ret:
    #    cv2.imwrite('image.png', frame)


    #cap.release()

    #image = cv2.imread('image.png')
    #Resize image for detection
    #image = cv2.resize(image, (640,480))

#END OF WEBCAM PORTION

#Detecting all the regions in the image that has pedestrians
(regions,_) = hog.detectMultiScale(image, winStride=(4,4), padding=(4,4), scale=1.05)

#Drawing the regions in the Image
for (x,y,w,h) in regions:
    cv2.rectangle(image, (x,y), (x+w,y+h), (0,0,255), 2)
    rects = np.array([x,y,x+w,y+h])

#Display the output image
cv2.imshow("Image", image)
cv2.waitKey(0)

#Save the output image
cv2.imwrite('pedestriantest_output.png', image);

cv2.destroyAllWindows()
