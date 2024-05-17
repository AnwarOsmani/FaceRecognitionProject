import cv2
import pickle
import os
import csv
import time
from datetime import datetime
from sklearn.neighbors import KNeighborsClassifier
from win32com.client import Dispatch

from FaceDetector import FaceDetector  

def speak(text):
    speaker = Dispatch(("SAPI.SpVoice"))
    speaker.Speak(text)

class FaceRecognition:
    def __init__(self):
        self._video = cv2.VideoCapture(0)
        self._img_background = cv2.imread("background.jpg")
        self._facedetect = FaceDetector()  
        self._windowName = "User Recognition"

        self._knn = None
        self._labels = None
        self._faces_data = None
        self._col_names = ['NAME', 'TIME']
        self._threshold = 4000  # Adjust this threshold value as needed

        if 'names.pkl' in os.listdir('data/') and 'faces_data.pkl' in os.listdir('data/'):
            with open('data/names.pkl', 'rb') as w:
                self._labels = pickle.load(w)
            with open('data/faces_data.pkl', 'rb') as f:
                self._faces_data = pickle.load(f)
            self._knn = KNeighborsClassifier(n_neighbors=5, metric='euclidean')  # Change metric as needed
            self._knn.fit(self._faces_data, self._labels)

    def recognize_faces(self):
        while True:
            ret, frame = self._video.read()
            k = cv2.waitKey(1)
            if k == ord('q'):
                self._close_camera()
                break
            if self._knn is None:
                cv2.putText(frame, "You are not registered", (100, 100), cv2.FONT_HERSHEY_COMPLEX, 1,
                            (255, 255, 255), 1)
                self._img_background[162:162 + 480, 55:55 + 640] = frame
                cv2.imshow(self._windowName, self._img_background)
            else:
                faces = self._facedetect.detect_faces(frame)
                for (x, y, w, h) in faces:
                    crop_img = frame[y:y + h, x:x + w, :]
                    resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
                    output = self._knn.predict(resized_img)
                    distances, neighbors = self._knn.kneighbors(resized_img)
                    min_distance = min(distances[0])
                    ts = time.time()
                    date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
                    timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")
                    exist = os.path.isfile("Attendance/Attendance_" + date + ".csv")
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
                    cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)

                    if min_distance <= self._threshold:  # Check if distance is within threshold
                        cv2.putText(frame, "Welcome " + str(output[0]), (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1,
                                    (255, 255, 255), 1)
                        attendance = [str(output[0]), str(timestamp)]
                        if k == ord('o'):
                            self._take_attendance(date, attendance, exist)
                            self._close_camera()
                            break
                    else:
                        cv2.putText(frame, "You are not registered", (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1,
                                    (255, 255, 255), 1)
                    self._img_background[162:162 + 480, 55:55 + 640] = frame
                    cv2.imshow(self._windowName, self._img_background)

    def _take_attendance(self, date, attendance, exist):
        speak("Attendance Taken..")
        time.sleep(1)
        if exist:
            with open("Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(attendance)
        else:
            with open("Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(self._col_names)
                writer.writerow(attendance)

    def _close_camera(self):
        self._video.release()
        cv2.destroyAllWindows()
