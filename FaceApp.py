import tkinter as tk
from tkinter import messagebox

from FaceDataCollector import FaceDataCollector
from FaceRecognition import FaceRecognition


class FaceApp:
    def __init__(self, root):
        self._root = root
        self._root.title("Face Recognition System")
        self._root.geometry("600x400")  # Set the window size here
        
        self._name_label = tk.Label(root, text="Enter your name:")
        self._name_entry = tk.Entry(root)
        self._show_registration_button = tk.Button(root, text="Registration", command=self._show_registraion_items)
        self._register_button = tk.Button(root, text="Register", command=self._register_face)
        self._attendance_button = tk.Button(root, text="Take Attendance", command=self._recognize_faces)
        self._quit_button = tk.Button(root, text="Quit", command=self._quit_program)
        
        # Coder information
        self._coder_info = tk.Label(root, text='Developed by: "Osmani" Mohammad Anwar')
        self._id_info = tk.Label(root, text='Student ID: 2120236001')

        # Packing widgets
        self._name_label.pack_forget()
        self._name_entry.pack_forget()
        self._show_registration_button.pack()
        self._attendance_button.pack(side="top")
        self._id_info.pack(side='bottom')
        self._coder_info.pack(side='bottom')
        self._quit_button.pack(side="bottom")

    def _show_registraion_items(self):
        self._name_label.pack()  # Display name label
        self._name_entry.pack()  # Display name entry field
        self._register_button.pack()
        self._show_registration_button.forget()
        
    def _register_face(self):
        name = self._name_entry.get()
        if name == "":
            messagebox.showerror("Error", "Please enter your name.")
            return
        face_data_collector = FaceDataCollector(name)
        face_data_collector.collect_data()
        face_data_collector.save_data()
        messagebox.showinfo("Success", "Face data collected and saved successfully.")
        self._name_label.forget()
        self._name_entry.forget()
        self._register_button.forget()
        self._show_registration_button.pack()

    def _recognize_faces(self):
        face_recognition = FaceRecognition()
        face_recognition.recognize_faces()

    def _quit_program(self):
        self._root.destroy()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = FaceApp(root)
    root.mainloop()
