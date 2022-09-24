import cv2
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image")
args = vars(ap.parse_args())

img = cv2.imread(args["image"])
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
haar = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
print("Anjay ganteng banget\n" * 5)

face = haar.detectMultiScale(gray, 1.3, 5)
for x, y, w, h in face:
    # cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
    # Alternative
    # img[y:y+h, x:x+w] = cv2.GaussianBlur(img[y:y+h, x:x+w], (41, 41), 5000)
    steps_count = 8
    stepsX = np.linspace(x, x + w, steps_count + 1, dtype=int)
    stepsY = np.linspace(y, y + h, steps_count + 1, dtype=int)
    for direction_x in range(steps_count):
        for direction_y in range(steps_count):
            color = cv2.mean(img[stepsY[direction_y]: stepsY[direction_y + 1],
                             stepsX[direction_x]: stepsX[direction_x + 1]])
            cv2.rectangle(img, (stepsX[direction_x], stepsY[direction_y]), (
                stepsX[direction_x + 1], stepsY[direction_y + 1]), color, -1)

cv2.imshow('Blurry Face', img)
cv2.imwrite("Blurry Face.jpg", img)
cv2.waitKey(0)
