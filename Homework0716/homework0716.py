# -*- coding: utf-8 -*-
"""Homework0716

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/145nT-oUVt9RfzHCUxWNPvR6dtnzysx0H
"""

# [1] 라이브러리 불러오기
import cv2
import os
import math
import shutil
from google.colab import files
from collections import defaultdict, deque

# [2] 차량 추적 클래스 정의
PIXEL_TO_METER = 0.05
FRAME_RATE = 30

class VehicleTracker:
    def __init__(self):
        self.vehicles = defaultdict(lambda: deque(maxlen=2))
        self.speeds = {}
        self.directions = {}

    def update(self, frame_id, detections):
        for vehicle_id, (x, y) in detections.items():
            self.vehicles[vehicle_id].append((frame_id, x, y))
            self._compute_speed_and_direction(vehicle_id)

    def _compute_speed_and_direction(self, vehicle_id):
        if len(self.vehicles[vehicle_id]) < 2:
            return
        (f1, x1, y1), (f2, x2, y2) = self.vehicles[vehicle_id]
        dt = (f2 - f1) / FRAME_RATE
        if dt == 0:
            return
        dx = (x2 - x1) * PIXEL_TO_METER
        dy = (y2 - y1) * PIXEL_TO_METER
        distance = math.sqrt(dx**2 + dy**2)
        speed = distance / dt
        angle = math.degrees(math.atan2(dy, dx))
        self.speeds[vehicle_id] = speed
        self.directions[vehicle_id] = angle

    def get_vehicle_info(self, vehicle_id):
        return {
            "speed_mps": self.speeds.get(vehicle_id),
            "direction_deg": self.directions.get(vehicle_id)
        }

# [3] 차량 감지 (밝은 영역 기반)
def detect_vehicles(frame):
    detections = {}
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    vehicle_id = 0
    for cnt in contours:
        if cv2.contourArea(cnt) > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            center_x, center_y = x + w // 2, y + h // 2
            detections[vehicle_id] = (center_x, center_y)
            vehicle_id += 1
    return detections

# [4] 이미지 업로드 (여러 장 직접 선택)
print(" 여러 장의 이미지(.jpg/.png)를 선택해서 업로드하세요")
uploaded = files.upload()

# [5] 이미지 저장 디렉토리 생성
upload_dir = "uploaded_images"
os.makedirs(upload_dir, exist_ok=True)

# 저장
for fname in uploaded:
    with open(os.path.join(upload_dir, fname), 'wb') as f:
        f.write(uploaded[fname])

# [6] 이미지 정렬
image_paths = sorted([
    os.path.join(upload_dir, f) for f in os.listdir(upload_dir)
    if f.lower().endswith(('.jpg', '.png'))
])
print(f" 총 {len(image_paths)}장의 이미지가 업로드되었습니다.")

# [7] 결과 프레임 디렉토리
result_dir = "result_frames"
os.makedirs(result_dir, exist_ok=True)

# [8] 차량 추적 및 시각화 프레임 저장
tracker = VehicleTracker()

for frame_id, path in enumerate(image_paths):
    frame = cv2.imread(path)
    detections = detect_vehicles(frame)
    tracker.update(frame_id, detections)

    for vid, (x, y) in detections.items():
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
        info = tracker.get_vehicle_info(vid)
        if info["speed_mps"] is not None:
            text = f"ID {vid} | {info['speed_mps']:.1f} m/s | {info['direction_deg']:.1f}°"
            cv2.putText(frame, text, (x+10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)

    cv2.imwrite(os.path.join(result_dir, f"frame_{frame_id:04d}.jpg"), frame)

# [9] 영상 생성
sample_frame = cv2.imread(os.path.join(result_dir, "frame_0000.jpg"))
height, width, _ = sample_frame.shape
video_path = "vehicle_tracking_result.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(video_path, fourcc, FRAME_RATE, (width, height))

for i in range(len(image_paths)):
    frame = cv2.imread(os.path.join(result_dir, f"frame_{i:04d}.jpg"))
    video.write(frame)

video.release()
print("영상 저장 완료:", video_path)

# [10] 다운로드 링크 생성
files.download(video_path)