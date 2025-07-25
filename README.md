# JeonBotDae-Project
전봇대 Project 수행
파일 업로드 및 간단한 설명

1. 객체 검출
이미지 또는 영상에서 특정 객체(예: 차량, 사람 등)를 위치와 함께 인식하는 기술.

고전 방법: 색상 필터, 경계선 추출, 히스토그램 기반 분석 등

최근 방식: CNN 기반의 YOLO, SSD, Faster R-CNN 등 딥러닝 모델 활용

2. 객체 추적
연속된 프레임에서 같은 객체를 식별하고 추적하는 기술

단일 객체 추적 (e.g., KCF, CSRT) 또는 다중 객체 추적 (e.g., SORT, DeepSORT)

차량 ID를 유지하며 움직임을 분석하는 데 사용

3. 영상 속도 계산
객체 위치의 시간에 따른 변화량을 통해 속도 추정
속도 = 이동 거리 / 시간

픽셀 단위 거리를 실제 거리(미터 등)로 바꾸기 위해 캘리브레이션 필요

4. 방향 추정 (Direction Estimation)
객체의 이동 방향을 벡터로 계산 후, 각도로 변환
atan2(dy, dx) → 방향 각도 (−180° ~ +180°)

5. 캘리브레이션 (Calibration)
이미지 좌표(pixels)를 실제 거리로 변환하기 위한 과정

간단한 경우: 1픽셀 = xx미터 비율 사용

정확한 경우: Homography 또는 카메라 내부/외부 파라미터 사용

6. 프레임 처리 및 영상 생성
영상은 여러 장의 이미지(프레임)로 구성됨
cv2.VideoWriter를 이용해 프레임을 .mp4로 변환 가능

#0726
실제 도로 영상을 기반으로 객체 탐지, 추적, 속도 계산, 충돌 예측까지 전 과정을 구현했습니다.

오픈소스 트래킹 라이브러리 없이 충돌 판단 로직을 직접 수식화하고 개발했습니다.

선형 경로 예측과 상대 속도 기반 충돌 시간 계산 공식을 적용하여 실제 차량 간 거리와 시간 개념을 추론했습니다.

YOLOv8 + Norfair를 연동하면서 프레임 처리 최적화, 속도 계산 안정화, 경고 로그 기록 등 전체 파이프라인을 구성했습니다.

경고 로그 기반으로 충돌 가능성이 있는 시점의 프레임만 자동 추출하는 기능을 추가해, 분석 효율을 높였습니다.


