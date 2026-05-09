import cv2
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
frames_dir = os.path.join(script_dir, "frames")
os.makedirs(frames_dir, exist_ok=True)

video_path = '/home/nour/Smart Parking YOLO/BLK-HDPTZ12 Security Camera Parkng Lot Surveillance Video [U7HRKjlXK-Y].mkv'
cap = cv2.VideoCapture(video_path)

count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if count % 10 == 0:
        cv2.imwrite(os.path.join(frames_dir, f"frame_{count}.jpg"), frame)

    count += 1

cap.release()