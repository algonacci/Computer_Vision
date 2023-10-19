import cv2

# Load the pre-trained face detection classifier
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Initialize the webcam (webcam index 0 by default)
cap = cv2.VideoCapture(0)

# Check if the webcam opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Check if the frame was read successfully
    if not ret:
        print("Error: Could not read frame.")
        break

    # Get the dimensions of the frame
    height, width, _ = frame.shape

    # Calculate the coordinates for the center box
    x = width // 4  # Start x-coordinate
    y = height // 4  # Start y-coordinate
    w = width // 2  # Width of the rectangle
    h = height // 2  # Height of the rectangle

    # Define the coordinates of the green box
    green_box = (x, y, x + w, y + h)

    # Draw the green box on the frame
    cv2.rectangle(frame, (x, y), (x + w, y + h),
                  (0, 255, 0), 2)  # (B, G, R), thickness=2

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform face detection only within the green box
    faces = face_cascade.detectMultiScale(
        gray[y:y + h, x:x + w], scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around detected faces within the green box
    for (fx, fy, fw, fh) in faces:
        cv2.rectangle(frame, (x + fx, y + fy), (x + fx + fw, y +
                      fy + fh), (0, 0, 255), 2)  # Red color for detected faces

    # Display the frame with face detection within the green box
    cv2.imshow('Face Detection within Green Box', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()
