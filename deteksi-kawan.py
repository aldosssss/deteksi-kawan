import cv2
import serial
import numpy as np
import time

#arduinoData = serial.Serial('/dev/ttyUSB0', 9600, timeout = 0.001)
cap = cv2.VideoCapture(1)
#cap1 = cv2.VideoCapture(1)
kamera = 'f'
terima = 'W'

def front():
    global kamera
    ret, img = cap.read()
    #cv2.imshow('original',img)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    lower_yellow = np.array ([69,79,149])
    upper_yellow = np.array ([104,172,255])
    edges = cv2.Canny(img, 15, 125)

    mask = cv2.inRange (hsv, lower_yellow, upper_yellow)
    
    kernel = np.ones((5,5), np.float32)/255
    #median = cv2.medianBlur(res, 15)
    iterations = 1
    dilation = cv2.dilate(mask, kernel, iterations)

    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    font=cv2.FONT_HERSHEY_COMPLEX
    contours,_ = cv2.findContours(closing.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours)>0:
        c = max(contours,key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        if M["m00"]==0:
            M["m00"]=1
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        x = int(M["m10"] / M["m00"])
        y = int(M["m01"] / M["m00"])
        if radius > 2:
            cv2.circle(img,(10,20), 10, (0,0,255), -1)
            cv2.putText(img, "D", (27, 25), font, 0.6, (0, 255, 0), 2)
            cv2.circle(img, (int(x), int(y)), int(radius),(0, 255, 0), 2)
            cv2.circle(img, (int(x), int(y)), 5, (0, 255, 255), -1)
            
        else :
            kamera = 'o'
    else:
        kamera = 'o'
        
    cv2.imshow('closing',closing)
    cv2.imshow('result',img)

while True:
    front()

    key=cv2.waitKey(1) & 0xFF
    if key==ord('q'):
        break
cv2.destroyAllWindows()
cap.release()
