import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from pythonosc import udp_client
import time
import random
dataX = 0
locY = 0
ip = "192.168.1.8"
port = 8888

client = udp_client.SimpleUDPClient(ip, port)

        
face_cascade = cv.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
cap = cv.VideoCapture(0)
while(True):
    # Capture frame-by-frame
    ret, img = cap.read()

    # Our operations on the frame come here
   
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 2)


    for (x,y,w,h) in faces:
        cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        print(int(x+w/2), int(y+h/2))
        dataX = int(x+w/2)
        client.send_message("/led", dataX)
        print(dataX)
        cv.circle(img,(int(x+w/2), int(y+h/2)), 3, (255, 0, 0), -1)
       
    # Display the resulting frame
    cv.imshow('frame',img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()

cv.imshow('img',img)
cv.waitKey(0)
cv.destroyAllWindows()
