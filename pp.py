import cv2
from serial import Serial
import os
import math
ser = Serial('/dev/cu.usbserial-120', 9600)
import time

def face_detect():
    

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        time.sleep(1)
        ret, img = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        

        for (x, y, w, h) in faces:
            
            #max 1500| -> 0 -> left
            into = ("t" + str(math.floor((x*0.1125))))
            print(into)
            ser.write(into.encode())
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)

        cv2.imshow('img', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    face_detect()