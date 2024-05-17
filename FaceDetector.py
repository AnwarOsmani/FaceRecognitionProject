import cv2


class FaceDetector:
    def __init__(self, cascade_file='data/haarcascade_frontalface_default.xml'):
        self.face_cascade = cv2.CascadeClassifier(cascade_file)

    def detect_faces(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        return faces
