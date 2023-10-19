from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2

# Construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
                help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
                help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.7,
                help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# Load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# Initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

# Define the coordinates for the Region of Interest (ROI) box
roi_x, roi_y, roi_w, roi_h = 300, 100, 400, 400

# Create a named window with a specific size
window_name = "Face Detection within Green Box"
# WINDOW_NORMAL allows resizing
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

# Loop over the frames from the video stream
while True:
    # Grab the frame from the threaded video stream and resize it
    frame = vs.read()
    frame = imutils.resize(frame, width=1000)

    # Get the frame dimensions
    (h, w) = frame.shape[:2]

    # Create a blob from the frame and pass it through the network
    blob = cv2.dnn.blobFromImage(cv2.resize(
        frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

    # Pass the blob through the network and obtain the detections and predictions
    net.setInput(blob)
    detections = net.forward()
    count = 0

    # Loop over the detections
    for i in range(0, detections.shape[2]):
        # Extract the confidence (i.e., probability) associated with the prediction
        confidence = detections[0, 0, i, 2]

        # Filter out weak detections by ensuring the `confidence` is greater than the minimum confidence
        if confidence < args["confidence"]:
            continue
        count += 1

        # Compute the (x, y)-coordinates of the bounding box for the object
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")

        # Check if the detected face is within the ROI
        if startX >= roi_x and startY >= roi_y and endX <= (roi_x + roi_w) and endY <= (roi_y + roi_h):
            # Draw the bounding box of the face along with the associated probability
            text = "{:.2f}%".format(confidence * 100) + ", Count " + str(count)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.rectangle(frame, (startX, startY),
                          (endX, endY), (0, 255, 0), 2)
            cv2.putText(frame, text, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)

    # Draw the ROI box on the frame
    cv2.rectangle(frame, (roi_x, roi_y),
                  (roi_x + roi_w, roi_y + roi_h), (0, 0, 255), 2)

    # Show the output frame
    cv2.imshow(window_name, frame)
    key = cv2.waitKey(1) & 0xFF

    # If the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# Do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
