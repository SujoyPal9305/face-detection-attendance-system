"""
Face Detection Attendance System - Main Application
Author: Sujoy Pal
"""

import cv2
import os
import sys
from datetime import datetime

# Import modules
from face_detection import FaceDetector
from face_recognition import FaceRecognizer
from attendance_logger import AttendanceLogger

class AttendanceSystem:
    def __init__(self):
        print("="*60)
        print("FACE DETECTION ATTENDANCE SYSTEM")
        print("="*60)
        
        try:
            self.face_detector = FaceDetector()
            self.face_recognizer = FaceRecognizer()
            self.attendance_logger = AttendanceLogger()
            print("[SUCCESS] All modules initialized successfully\n")
        except Exception as e:
            print(f"[ERROR] Initialization failed: {e}")
            sys.exit(1)
    
    def display_menu(self):
        print("\n" + "="*60)
        print("MAIN MENU")
        print("="*60)
        print("1. Register New User")
        print("2. Start Attendance (Webcam)")
        print("3. View Today's Attendance")
        print("4. List Registered Users")
        print("5. Delete User")
        print("6. Test Face Detection")
        print("0. Exit")
        print("="*60)
    
    def register_new_user(self):
        print("\n--- REGISTER NEW USER ---")
        name = input("Enter name: ").strip()
        
        if not name:
            print("[ERROR] Name cannot be empty")
            return
        
        if name in self.face_recognizer.known_face_names:
            print(f"[WARNING] {name} is already registered")
            choice = input("Re-register? (y/n): ").lower()
            if choice != 'y':
                return
            self.face_recognizer.delete_user(name)
        
        success = self.face_recognizer.register_face(name)
        if not success:
            print("[ERROR] Registration failed")
    
    def start_attendance_webcam(self):
        print("\n--- ATTENDANCE MODE ---")
        print("[INFO] Starting webcam... Press 'q' to quit")
        print("[INFO] Attendance will be marked automatically\n")
        
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("[ERROR] Could not open webcam")
            return
        
        recently_marked = {}
        cooldown_seconds = 10
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            if frame_count % 5 == 0:
                results = self.face_recognizer.recognize_faces(frame)
                
                for (name, face_location, confidence) in results:
                    top, right, bottom, left = face_location
                    
                    if name != "Unknown":
                        color = (0, 255, 0)
                        label = f"{name} ({confidence*100:.1f}%)"
                        
                        current_time = datetime.now()
                        if name not in recently_marked or \
                           (current_time - recently_marked[name]).seconds > cooldown_seconds:
                            if self.attendance_logger.mark_attendance(name):
                                recently_marked[name] = current_time
                                cv2.putText(frame, "ATTENDANCE MARKED!", (10, 90),
                                          cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    else:
                        color = (0, 0, 255)
                        label = "Unknown"
                    
                    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                    cv2.putText(frame, label, (left + 6, bottom - 6),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            cv2.putText(frame, f"Registered: {len(self.face_recognizer.known_face_names)}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, f"Present: {len(self.attendance_logger.today_attendance)}", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "Press 'q' to quit", (10, frame.shape[0] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow('Attendance System', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        print("\n[INFO] Attendance session ended")
    
    def view_today_attendance(self):
        print("\n--- TODAY'S ATTENDANCE ---")
        self.attendance_logger.display_today_attendance()
    
    def list_registered_users(self):
        print("\n--- REGISTERED USERS ---")
        self.face_recognizer.list_users()
    
    def delete_user(self):
        print("\n--- DELETE USER ---")
        self.face_recognizer.list_users()
        
        if len(self.face_recognizer.known_face_names) == 0:
            return
        
        name = input("\nEnter name to delete: ").strip()
        if not name:
            print("[ERROR] Name cannot be empty")
            return
        
        confirm = input(f"Delete {name}? (y/n): ").lower()
        if confirm == 'y':
            self.face_recognizer.delete_user(name)
    
    def test_face_detection(self):
        print("\n--- TEST FACE DETECTION ---")
        print("[INFO] Starting webcam... Press 'q' to quit")
        self.face_detector.detect_from_webcam()
    
    def run(self):
        while True:
            self.display_menu()
            
            try:
                choice = input("\nEnter your choice: ").strip()
                
                if choice == '1':
                    self.register_new_user()
                elif choice == '2':
                    self.start_attendance_webcam()
                elif choice == '3':
                    self.view_today_attendance()
                elif choice == '4':
                    self.list_registered_users()
                elif choice == '5':
                    self.delete_user()
                elif choice == '6':
                    self.test_face_detection()
                elif choice == '0':
                    print("\n[INFO] Exiting... Goodbye!")
                    break
                else:
                    print("[ERROR] Invalid choice")
            
            except KeyboardInterrupt:
                print("\n\n[INFO] Interrupted. Exiting...")
                break
            except Exception as e:
                print(f"\n[ERROR] {e}")

def main():
    try:
        system = AttendanceSystem()
        system.run()
    except Exception as e:
        print(f"[FATAL ERROR] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
