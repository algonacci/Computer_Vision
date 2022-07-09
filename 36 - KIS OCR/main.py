import easyocr
import cv2

img = cv2.imread('KIS.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
spacer = 50
reader = easyocr.Reader(['id'], gpu=True)
result = reader.readtext(img)
result

data = []

for detection in result: 
    top_left = tuple(detection[0][0])
    bottom_right = tuple(detection[0][2])
    text = detection[1]
    img = cv2.rectangle(img,top_left,bottom_right,(0,255,0),3)
    data.append(text)
    print(text)
    spacer+=15
cv2.imshow('',img)
cv2.waitKey(0)
