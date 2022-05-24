import cv2
import matplotlib.pyplot as plt

plt.rcParams.update({
    "lines.color": "white",
    "patch.edgecolor": "white",
    "text.color": "white",
    "axes.facecolor": "black",
    "axes.edgecolor": "white",
    "axes.labelcolor": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "grid.color": "grey",
    "figure.facecolor": "black",
    "figure.edgecolor": "black",
    "savefig.facecolor": "black",
    "savefig.edgecolor": "black"})

image = cv2.imread('male.jpg')

grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
grayscale = cv2.medianBlur(grayscale, 7)
edge = cv2.adaptiveThreshold(grayscale, 350, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2.5)

cv2.imshow("Original image", image)
cv2.imshow("Edge detection", edge)
cv2.imwrite("Original image.jpg", image)
cv2.imwrite("Edge detection.jpg", edge)


cv2.waitKey()