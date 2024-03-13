import cv2
from ultralytics import YOLO
import torch
import numpy as np
from ultralytics.utils.plotting import Annotator, colors
import asyncio
from make_points import select_danger_points

# CUDA 장치 사용 비활성화
torch.backends.cudnn.enabled = False
torch.cuda.is_available = lambda : False

model = YOLO("./modelStorage/CAIROSS_model.pt")
names = model.names

danger_points = []
person_box_frame = []

def stream_detected_frames(video_path):
    global person_box_frame, danger_points
    # 동영상 파일 열기
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        success, frame = cap.read()

        person_box_frame = frame.copy()

        if success:
            # 이미지 크기를 가져와서 빈 흑백 이미지 생성
            height, width = frame.shape[:2]
            combined_mask = np.zeros((height, width), dtype=np.uint8)

            results = model(frame, verbose=False, conf = 0.4)

            all_contours_with_labels = []

            # 사람만 박스로 보여주기
            boxes = results[0].boxes.xyxy.cpu().tolist()
            clss = results[0].boxes.cls.cpu().tolist()
            annotator = Annotator(frame, line_width=2, example=names)

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

            if boxes is not None:
                for box, cls in zip(boxes, clss):
                    if cls == 1:
                        annotator.box_label(box, color=(255, 0,0), label=names[int(cls)])  # 파란색으로 변경

            for r in results:
                # iterate each object contour
                for ci, c in enumerate(r):
                    # label 가져오기
                    label = c.names[c.boxes.cls.tolist().pop()]

                    if label == 'handrail':
                        # Create contour mask
                        contour = c.masks.xy.pop().astype(np.int32).reshape(-1, 1, 2)
                        mask = np.zeros((height, width), dtype=np.uint8)
                        cv2.drawContours(mask, [contour], -1, (255, 255, 255), 3)  # 테두리만 그리기

                        # 마스크를 누적하여 합치기
                        combined_mask = cv2.bitwise_or(combined_mask, mask)

                        M = cv2.moments(contour)

                        if M["m00"] != 0:
                            cx = int(M["m10"] / M["m00"])
                            cy = int(M["m01"] / M["m00"])
                            # 중심점에 라벨 추가
                            box_color = (255, 255, 255)  # 파란색

                            # 투명한 사각형 이미지 생성
                            overlay = frame.copy()
                            cv2.rectangle(overlay, (cx - 90, cy - 130), (cx + 60, cy - 90), box_color, -1)

                            # 이미지 합성
                            alpha = 0.5  # 투명도 값 (0.0은 완전 투명, 1.0은 완전 불투명)
                            frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

                            # cv2.putText(frame, label, (cx, cy - 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                            cv2.putText(frame, label, (cx - 80, cy - 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

            # 원본 이미지에 마스크 적용
            masked_img = frame.copy()
            # 마스크가 적용된 부분은 빨간색으로, 녹색 채널은 0으로, 파란색 채널은 빨간색과 같은 값으로 설정
            masked_img[:, :, 2] = np.where(combined_mask == 255, 255, masked_img[:, :, 2])  # 빨간색 채널에 마스크 적용
            masked_img[:, :, 1] = np.where(combined_mask == 255, 80, masked_img[:, :, 1])  # 녹색 채널에 마스크 적용
            masked_img[:, :, 0] = np.where(combined_mask == 255, 100, masked_img[:, :, 0])  # 파란색 채널에 마스크 적용 (빨간색 강조)

        # 마스크된 이미지를 생성하고 전송
        success, buffer = cv2.imencode('.jpg', masked_img)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(frame_bytes) + b'\r\n')

def get_signal():
    global danger_points
    new_points = []  # 빈 리스트로 초기화
    if danger_points:
        for point in danger_points:
            new_points.append({'w': int(point[0]), 'h': int(point[1])})
    return new_points

def generate_frames():
    global person_box_frame
    print(len(person_box_frame))
    while True:
        success, buffer = cv2.imencode('.jpg', person_box_frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                bytearray(frame_bytes) + b'\r\n')

