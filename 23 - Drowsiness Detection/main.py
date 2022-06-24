import cv2
import mediapipe as mp
import itertools
import module

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(0)

i = 0
second = 1
EAR = []
EAR_FIX = 0
EAR_ALL = []
fps = cap.get(cv2.CAP_PROP_FPS)
fps = int(fps)

with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image)

        # Draw the face mesh annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_contours_style())
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_iris_connections_style())

                iris_index = list(
                    set(itertools.chain(*mp_face_mesh.FACEMESH_IRISES)))
                list_z = []
                for iris in iris_index:
                    z = round(face_landmarks.landmark[iris].z, 3)
                    list_z.append(z)
                focus = module.check_focus(list_z)

                # Get Point on left eye
                point = face_landmarks.landmark[159]
                point1 = face_landmarks.landmark[145]
                distance_left = module.euclaideanDistance(point, point1)

                # Get Point on right eye
                point = face_landmarks.landmark[386]
                point1 = face_landmarks.landmark[374]
                distance_right = module.euclaideanDistance(point, point1)

                # Check if the eye is closed or not.
                close_eyes = module.check_close_eyes(
                    distance_left, distance_right)

                cv2.rectangle(image, (0, 0), (170, 80), (0, 0, 0), -1)
                if(focus == True and close_eyes == False):
                    cv2.putText(image, text="Steady", org=(15, 35), fontFace=cv2.FONT_HERSHEY_DUPLEX,
                                fontScale=1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
                    EAR.append(1)
                else:
                    cv2.putText(image, text="Drowsy", org=(15, 35), fontFace=cv2.FONT_HERSHEY_DUPLEX,
                                fontScale=1, color=(0, 0, 255), thickness=2, lineType=cv2.LINE_AA)
                    EAR.append(0)

        else:
            cv2.rectangle(image, (0, 0), (250, 80), (0, 0, 0), -1)
            cv2.putText(img=image, text="Face Not Detected", org=(
                10, 35), fontFace=1, fontScale=1.5, color=(0, 0, 255), thickness=2)

        i = i+1
        if(i == fps):
            EAR_SUM = sum(EAR)
            EAR_FIX = EAR_SUM/fps
            EAR_ALL.append([second, EAR_FIX])
            EAR = []
            i = 0
            second = second+1
            print('Eye Aspect Ratio: {}'.format(EAR_FIX))

        if (EAR_FIX > 0.3):
            cv2.putText(img=image, text="EAR: "+str(round(EAR_FIX, 2) * 100) + "%",
                        org=(10, 70), fontFace=1, fontScale=1.5, color=(255, 255, 0), thickness=2)
        else:
            cv2.putText(img=image, text="EAR: "+str(round(EAR_FIX, 2) * 100) + "%",
                        org=(10, 70), fontFace=1, fontScale=1.5, color=(0, 0, 255), thickness=2)

        cv2.imshow('Drowsiness Detection', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
