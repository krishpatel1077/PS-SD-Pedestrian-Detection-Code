import cv2
import imutils
import numpy as np

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

image = cv2.imread('HDRfastfocus2.jpg')
#Resize image for detection
image = cv2.resize(image, (640,480))
#Detecting all the regions in the image that has pedestrians
(regions,_) = hog.detectMultiScale(image, winStride=(4,4), padding=(4,4), scale=1.05)
for (x,y,w,h) in regions:
    cv2.rectangle(image, (x,y), (x+w,y+h), (0,0,255), 2)
    rects = np.array([x,y,x+w,y+h])

#Display the output image
cv2.imshow("Image", image)
cv2.waitKey(0)

#Save the output image
cv2.imwrite('pedestriantest_output.png', image);

cv2.destroyAllWindows()
