import cv2
import imutils
import numpy as np


#HOGDescriptptor - structure identifying feature used by openCV
#For purpose of this code, using default people detection pkg
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

#read test image
#image = cv2.imread('pedestrian-header3.png')

#COMMENTED PORTION FROM LINES 13 - 27 SHOW WEBCAM INPUT WITH PEDESTRIAN DETECTION
#CAN NOT BE TESTED IN FULL UNTIL RPI CAM IS AVAILABLE

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
if ret:
    cv2.imwrite('image.png', frame)


cap.release()

image = cv2.imread('image.png')
#Resize image for detection
image = cv2.resize(image, (640,480))

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
