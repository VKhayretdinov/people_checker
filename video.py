import cv2


def show_video():
    """
    Show video from webcam with face detection

    :return:
    """

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalcatface.xml')
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.02, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow('gray', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
