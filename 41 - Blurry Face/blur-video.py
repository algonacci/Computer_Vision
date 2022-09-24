import cv2
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True,
                help="path to input video")
args = vars(ap.parse_args())

# cam = cv2.VideoCapture(args["video"])
haar = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
font = cv2.FONT_HERSHEY_SIMPLEX

cam = cv2.VideoCapture(0)
cam.set(3, 640)  # set video widht
cam.set(4, 480)  # set video height

minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

while True:
    ret, img = cam.read()
    faces = haar.detectMultiScale(
        img,
        scaleFactor=1.5,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )

    for x, y, w, h in faces:
        try:
            img[y:y+h, x:x +
                w] = cv2.GaussianBlur(img[y:y+h, x:x+w], (41, 41), 5000)
            # cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        except:
            pass

    cv2.imshow('Blurry Face', img)
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break

cam.release()
cv2.destroyAllWindows()
