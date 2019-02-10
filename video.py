import cv2
from threading import Thread
import asyncio
import photo
import time


def face_detection_cascade(show_video=True):
    """
    Show video from webcam with face detection

    :return:
    """

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalcatface.xml')
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.02, 5)  # set that params for bigger chance to recognize a face

        if show_video:
            for (x, y, w, h) in faces:
                cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 0, 0), 2)

            cv2.imshow('gray', gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()


def face_detection_dnn(vk, user_id):
    model = cv2.dnn.readNetFromCaffe("caffe/deploy.prototxt", "caffe/mobilenet_iter_73000.caffemodel")
    cap = cv2.VideoCapture(0)

    is_sended = False

    print("SHOW VIDEO")
    while True:
        ret, frame = cap.read()
        frame_resized = cv2.resize(frame, (300, 300))  # Resize frame for prediction

        blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5), False)
        model.setInput(blob)
        detections = model.forward()

        cols = frame_resized.shape[1]
        rows = frame_resized.shape[0]

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]  # Confidence of prediction
            if confidence > 0.2:  # Filter prediction
                person_id = 15
                class_id = int(detections[0, 0, i, 1])  # Class label
                # Object location
                x_left_bottom = int(detections[0, 0, i, 3] * cols)
                y_left_bottom = int(detections[0, 0, i, 4] * rows)
                x_right_top = int(detections[0, 0, i, 5] * cols)
                y_right_top = int(detections[0, 0, i, 6] * rows)  # Factor for scale to original size of frame
                height_factor = frame.shape[0] / 300.0
                width_factor = frame.shape[1] / 300.0
                # Scale object detection to frame
                x_left_bottom = int(width_factor * x_left_bottom)
                y_left_bottom = int(height_factor * y_left_bottom)
                x_right_top = int(width_factor * x_right_top)
                y_right_top = int(height_factor * y_right_top)

                # Draw location of object
                if class_id == person_id:
                    cv2.rectangle(frame, (x_left_bottom, y_left_bottom), (x_right_top, y_right_top),
                                  (0, 255, 0), 2)

                    if not is_sended:
                        the_photo = "images/" + str(0) + ".jpg"
                        cv2.imwrite(the_photo, frame)
                        photo.get_take_photo(vk, the_photo, user_id)
                        is_sended = True
                else:
                    is_sended = False

        cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) >= 0:  # Break with ESC
            break


