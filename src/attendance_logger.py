"""
Attendance Logger Module
"""

import csv
import os
from datetime import datetime
from pathlib import Path

class AttendanceLogger:
    def __init__(self, attendance_file="data/attendance.csv"):
        self.attendance_file = attendance_file
        self.today_attendance = set()
        
        Path(os.path.dirname(attendance_file)).mkdir(parents=True, exist_ok=True)
        
        if not os.path.exists(attendance_file):
            self.create_attendance_file()
        
        self.load_today_attendance()
        print("[INFO] Attendance logger initialized")
    
    def create_attendance_file(self):
        with open(self.attendance_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Date', 'Time', 'Status'])
        print(f"[INFO] Created attendance file")
    
    def mark_attendance(self, name, status="Present"):
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        
        if name in self.today_attendance:
            print(f"[INFO] {name} already marked present today")
            return False
        
        with open(self.attendance_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([name, current_date, current_time, status])
        
        self.today_attendance.add(name)
        print(f"[SUCCESS] Attendance marked for {name} at {current_time}")
        return True
    
    def load_today_attendance(self):
        if not os.path.exists(self.attendance_file):
            return
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        try:
            with open(self.attendance_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['Date'] == current_date:
                        self.today_attendance.add(row['Name'])
        except:
            pass
    
    def display_today_attendance(self):
        current_date = datetime.now().strftime("%Y-%m-%d")
        print(f"\n{'='*60}")
        print(f"TODAY'S ATTENDANCE ({current_date})")
        print(f"{'='*60}")
        print(f"Total Present: {len(self.today_attendance)}")
        for name in self.today_attendance:
            print(f"  - {name}")
        print(f"{'='*60}\n")

if __name__ == "__main__":
    print("Testing Attendance Logger...")
    logger = AttendanceLogger()
    logger.mark_attendance("Test User")
    logger.display_today_attendance()
