import cv2
cap = cv2.VideoCapture(1)
while True:
    ret, frame = cap.read()
    HSV_Image=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    cv2.imshow('Webcam', HSV_Image)
    
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
