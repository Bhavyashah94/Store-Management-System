import cv2
import face_recognition
import sqlite3
import numpy as np
import threading
import queue
import tkinter as tk
from tkinter import simpledialog

db_path = "./Database/faces.db"
face_encodings = []
face_names = []
face_locations = []
face_labels = []
lock = threading.Lock()
face_queue = queue.Queue()  # Queue for handling new face entries

def initialize_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            roll_no TEXT,
            email TEXT,
            encoding BLOB
        )
    """)
    conn.commit()
    conn.close()

def load_known_faces():
    global face_encodings, face_names
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, encoding FROM users")
    rows = cursor.fetchall()
    conn.close()

    face_encodings.clear()
    face_names.clear()

    for name, encoding_blob in rows:
        if encoding_blob:
            face_encodings.append(np.frombuffer(encoding_blob, dtype=np.float64))
            face_names.append(name)

def add_new_face(face_enc):
    """ Runs Tkinter dialog in the main thread to get user input. """
    root = tk.Tk()
    root.withdraw()  # Hide main window

    name = simpledialog.askstring("New Face Detected", "Enter Name:")
    roll_no = simpledialog.askstring("New Face Detected", "Enter Roll No:")

    if name and roll_no:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, roll_no, encoding) VALUES (?, ?, ?)",
                       (name, roll_no, face_enc.tobytes()))
        conn.commit()
        conn.close()

        load_known_faces()  # Reload database after adding
        print(f"New face added: {name}")

def process_new_faces():
    """ Checks queue for new faces and processes them in the main thread. """
    while not face_queue.empty():
        face_enc = face_queue.get()
        add_new_face(face_enc)

def recognize_faces(frame):
    """ Runs face recognition in a separate thread without blocking video. """
    global face_locations, face_labels

    # Downscale for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detect faces & encode
    locations = face_recognition.face_locations(rgb_small_frame)
    encodings = face_recognition.face_encodings(rgb_small_frame, locations)

    labels = []
    for face_enc in encodings:
        matches = face_recognition.compare_faces(face_encodings, face_enc)
        name = "Unknown"

        if True in matches:
            face_distances = face_recognition.face_distance(face_encodings, face_enc)
            best_match_index = np.argmin(face_distances)
            if face_distances[best_match_index] < 0.5:
                name = face_names[best_match_index]
        else:
            # Add new face encoding to queue (processed in main thread)
            face_queue.put(face_enc)

        labels.append(name)

    # Scale back locations
    scaled_locations = [(top * 4, right * 4, bottom * 4, left * 4) for top, right, bottom, left in locations]

    # Update global variables safely
    with lock:
        face_locations = scaled_locations
        face_labels = labels

def capture_and_recognize():
    cap = cv2.VideoCapture(0)
    threading.Thread(target=recognize_faces, args=(np.zeros((480, 640, 3), dtype=np.uint8),), daemon=True).start()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Display raw video instantly
        cv2.imshow("Face Recognition", frame)

        # Process new faces in the main thread
        process_new_faces()

        # Draw bounding boxes (updated asynchronously)
        with lock:
            for (top, right, bottom, left), name in zip(face_locations, face_labels):
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Show overlayed frame
        cv2.imshow("Face Recognition", frame)

        # Start face recognition thread if idle
        if not threading.active_count() > 2:
            threading.Thread(target=recognize_faces, args=(frame.copy(),), daemon=True).start()

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    initialize_db()
    load_known_faces()
    capture_and_recognize()
