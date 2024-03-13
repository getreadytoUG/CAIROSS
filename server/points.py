import os
import cv2
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
import cv2
from ultralytics import YOLO
import torch
from make_points import select_danger_points


# CUDA 장치 사용 비활성화
torch.backends.cudnn.enabled = False
torch.cuda.is_available = lambda : False

# 모델 파일 경로 설정
model_path = os.path.join(os.getcwd(), 'modelStorage', 'CAIROSS_model.pt')

# 모델 불러오기
model = YOLO(model_path, verbose=False)

video_path = "./videoStorage/video.mp4" 

cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        results = model(frame, conf=0.3)

        # 마스크 초기화
        combined_mask = np.zeros_like(results[0].orig_img[:, :, 0], dtype=np.uint8)

        # 결과 저장 리스트
        all_contours_with_labels = []

        for result in results:
            img = np.copy(result.orig_img)
            labels = result.boxes.cls
            index = 0

            for i in result:
                b_mask = np.zeros(img.shape[:2], np.uint8)

                contour = i.masks.xy.pop()
                contour = contour.astype(np.int32)
                contour = contour.reshape(-1, 1, 2)

                combined_mask = np.maximum(combined_mask, b_mask)
                all_contours_with_labels.append({"contour": contour, "label": i.names[labels[index].item()]})
                index += 1                

        danger_points = select_danger_points(all_contours_with_labels)