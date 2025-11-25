"""
Face Recognition Module (Simple Template Matching)
"""

import cv2
import os
from pathlib import Path

class FaceRecognizer:
    def __init__(self, data_dir="data/faces"):
        self.data_dir = data_dir
        self.known_face_names = []
        self.known_face_images = []
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        Path(data_dir).mkdir(parents=True, exist_ok=True)
        self.load_faces()
        
        print(f"[INFO] Face recognizer initialized with {len(self.known_face_names)} registered users")
    
    def load_faces(self):
        self.known_face_names = []
        self.known_face_images = []
        
        if os.path.exists(self.data_dir):
            for filename in os.listdir(self.data_dir):
                if filename.endswith('.jpg'):
                    name = filename[:-4]
                    image_path = os.path.join(self.data_dir, filename)
                    face_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                    if face_img is not None:
                        self.known_face_names.append(name)
                        self.known_face_images.append(face_img)
    
    def register_face(self, name):
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("[ERROR] Could not open webcam")
            return False
        
        print(f"[INFO] Registering {name}... Press 's' to capture, 'q' to cancel")
        
        captured = False
        while not captured:
            ret, frame = cap.read()
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            cv2.putText(frame, f"Registering: {name}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, "Press 's' to capture", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.imshow('Register Face', frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('s'):
                if len(faces) > 0:
                    (x, y, w, h) = faces[0]
                    face_roi = gray[y:y+h, x:x+w]
                    face_roi = cv2.resize(face_roi, (200, 200))
                    
                    face_image_path = os.path.join(self.data_dir, f"{name}.jpg")
                    cv2.imwrite(face_image_path, face_roi)
                    captured = True
                    print(f"[SUCCESS] {name} registered successfully!")
                else:
                    print("[WARNING] No face detected. Try again.")
            elif key == ord('q'):
                print("[INFO] Registration cancelled")
                cap.release()
                cv2.destroyAllWindows()
                return False
        
        cap.release()
        cv2.destroyAllWindows()
        self.load_faces()
        return True
    
    def recognize_faces(self, image):
        if len(self.known_face_names) == 0:
            return []
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        results = []
        
        for (x, y, w, h) in faces:
            face_roi = gray[y:y+h, x:x+w]
            face_roi = cv2.resize(face_roi, (200, 200))
            
            best_match = "Unknown"
            best_score = 0
            
            for known_name, known_face in zip(self.known_face_names, self.known_face_images):
                result = cv2.matchTemplate(face_roi, known_face, cv2.TM_CCOEFF_NORMED)
                score = result[0][0]
                
                if score > best_score and score > 0.6:
                    best_score = score
                    best_match = known_name
            
            face_location = (y, x+w, y+h, x)
            results.append((best_match, face_location, best_score))
        
        return results
    
    def list_users(self):
        if len(self.known_face_names) == 0:
            print("[INFO] No registered users")
        else:
            print(f"[INFO] Registered users ({len(self.known_face_names)}):")
            for i, name in enumerate(self.known_face_names, 1):
                print(f"  {i}. {name}")
    
    def delete_user(self, name):
        if name in self.known_face_names:
            image_path = os.path.join(self.data_dir, f"{name}.jpg")
            if os.path.exists(image_path):
                os.remove(image_path)
            self.load_faces()
            print(f"[SUCCESS] {name} deleted successfully")
            return True
        else:
            print(f"[ERROR] {name} not found")
            return False

if __name__ == "__main__":
    print("Testing Face Recognition Module...")
    recognizer = FaceRecognizer()
    recognizer.list_users()
