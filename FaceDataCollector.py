import cv2
import numpy as np
import os
import pickle

from FaceDetector import FaceDetector  # Assuming you have a FaceDetector module

class FaceDataCollector:
    def __init__(self, name):
        self._video = cv2.VideoCapture(0)
        self._facedetect = FaceDetector()
        self._faces_data = []
        self._name = name
        self._img_background = cv2.imread("Registration Background.jpg")
        self._i = 0

    def collect_data(self):
        while True:
            ret, frame = self._video.read()
            faces = self._facedetect.detect_faces(frame)
            for (x, y, w, h) in faces:
                crop_img = frame[y:y+h, x:x+w]
                resized_img = cv2.resize(crop_img, (50, 50))
                if self._i % 3 == 0 and len(self._faces_data) < 30:  # Check the size of faces_data
                    self._faces_data.append(resized_img)
                self._i += 1
                cv2.putText(frame, 'Scanning...', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 1)
            self._img_background[162:162 + 480, 55:55 + 640] = frame
            cv2.imshow("User Registration", self._img_background)
            
            if (cv2.waitKey(1) & 0xFF == ord('q')) or len(self._faces_data) >= 30:  # Modify condition to exit loop
                self._video.release()
                cv2.destroyAllWindows()
                break

    def save_data(self):
        faces_data = np.asarray(self._faces_data)
        faces_data = faces_data.reshape(len(self._faces_data), -1)

        if 'names.pkl' not in os.listdir('data/'):
            names = [self._name] * len(self._faces_data)
            with open('data/names.pkl', 'wb') as f:
                pickle.dump(names, f)
        else:
            with open('data/names.pkl', 'rb') as f:
                names = pickle.load(f)
            names = names + [self._name] * len(self._faces_data)
            with open('data/names.pkl', 'wb') as f:
                pickle.dump(names, f)

        if 'faces_data.pkl' not in os.listdir('data/'):
            with open('data/faces_data.pkl', 'wb') as f:
                pickle.dump(faces_data, f)
        else:
            with open('data/faces_data.pkl', 'rb') as f:
                faces = pickle.load(f)
            faces = np.append(faces, faces_data, axis=0)
            with open('data/faces_data.pkl', 'wb') as f:
                pickle.dump(faces, f)
