# 🪽 CAIROSS
#### 교량 위 위험 행동 방지 및 빠른 초동조치를 위한 CCTV 분석 AI 서비스
#### 기간 : 2024-02-21 ~ 2024-03-07

----------------

## 🎁 기획
### "CAIROSS: Cliff Alarm Item for Rescue Of Severe Situation"
- "CAIROSS"는 다리 위 CCTV를 통해 투신 등의 위험행동을 감지하고 신속하게 대응하는 AI 기반 분석 서비스입니다
-  실시간 영상 분석을 통해 난간과 사람 사이의 거리를 측정하여 위험 상황을 판단하고, 관리자에게 알림을 주며 안전한 공공환경을 조성합니다.
- 자살 시도 후 실패한 사람들은 후회와 깨달음을 통해 삶의 가치를 깨달을 수 있고, 이 마지막 기회를 기회의 신 카이로스처럼 주고자 합니다. 

<img width="100%" alt="image" src="https://github.com/getreadytoUG/CAIROSS/assets/127275992/58fe1337-18aa-44d3-a5d4-ebb4ddeaba43">

<hr>

## 👨‍💻 My Role in Process
##### - 기획 및 아이디어 제공, YOLOv8s-seg 모델 학습, roboflow를 통한 데이터 정제, 알고리즘 제작

-------------------

## 🛍️ Dataset & Model
### 📚 Dataset
- [AI Hub "보행 안전을 위한 도로 시설물 데이터"](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=513)
- [roboflow "Roboflow Universe Instance Segmentation Dataset](https://universe.roboflow.com/)
- 전국 CCTV 데이터(직접 라벨링 후 제작)

<img width="100%" alt="image" src="https://github.com/getreadytoUG/CAIROSS/assets/127275992/68173dc9-237a-481c-b3f6-eff948a71e0d">
<img width="100%" alt="image" src="https://github.com/getreadytoUG/CAIROSS/assets/127275992/92d3c0fe-ff89-4942-848a-8284cee04178">

### 💻 Model
- **YOLOv8s-seg**

<img width="100%" alt="image" src="https://github.com/getreadytoUG/CAIROSS/assets/127275992/b7c8b011-d55a-41ae-98fb-1eda6f57fd63">
<img width="100%" alt="image" src="https://github.com/getreadytoUG/CAIROSS/assets/127275992/7a9d5e35-bd6a-41e0-99a0-01ffdbff8fad">
<img width="100%" alt="image" src="https://github.com/getreadytoUG/CAIROSS/assets/127275992/aeb04dc2-faf3-4998-84c0-374eec3d4ab3">

-------------------

## 🖥️ Server
- 교량을 촬영한 CCTV 가 영상을 서버로 송출
- 해당 영상을 CAIROSS 모델이 처리
- 사용자에게는 영상을 지속적으로 보여주며 위험 인물이 있다고 판단될 경우 해당 인물과 그 주위를 확대

<img width="100%" alt="image" src="https://github.com/getreadytoUG/CAIROSS/assets/127275992/9eb0d75d-cea5-4237-8fc2-aaa3e6118bde">

-------------------

## 🧑‍💻 Algorithm
- CCTV 에서는 사람 객체와 난간 사이의 거리를 정확히 측정할 수 없었습니다.(~~우리의 기술로는...~~)
- 그래서 직접 특정 알고리즘을 만들어서 사람과 난간사이의 거리를 측정할 필요가 있었습니다.
<img width="100%" alt="image" src="https://github.com/getreadytoUG/CAIROSS/assets/127275992/078ffd21-1ae9-48cf-ac5e-ec664c7cb9b5">
<img width="100%" alt="image" src="https://github.com/getreadytoUG/CAIROSS/assets/127275992/ea5ba7fb-0e48-48a1-baf4-be54a2bb6de9">
<img width="100%" alt="image" src="https://github.com/getreadytoUG/CAIROSS/assets/127275992/a483fc44-03a8-4bcb-914e-974890ca5495">
<img width="100%" alt="image" src="https://github.com/getreadytoUG/CAIROSS/assets/127275992/c5c5ceda-8c6e-42bb-ac2a-4b33aed82bd4">
<img width="100%" alt="image" src="https://github.com/getreadytoUG/CAIROSS/assets/127275992/c3403a2e-c603-4949-88b1-be2d98f956da">

----------------------------------------------

##### 📦 최종 서비스 형태

<img width="100%" alt="image" src="https://github.com/getreadytoUG/CAIROSS/assets/127275992/3a003b48-285d-4296-9482-8d1843ee776c">
<img width="100%" alt="image" src="https://github.com/getreadytoUG/CAIROSS/assets/127275992/aa648ae6-a948-42dd-b417-fc8c567cbea3">

------------------------------------------------

<img width="100%" alt="image" src="https://github.com/getreadytoUG/CAIROSS/assets/127275992/26ce562f-b8f2-4851-9f32-c54a1c77d0a5">

---------------------------------------------------

### ⚙️ Skills & Tools

<p align="center">
  <img src="https://img.shields.io/badge/Git-F05032?style=flat-square&logo=Git&logoColor=white"/>
  <img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=GitHub&logoColor=white"/>
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=CSS3&logoColor=white"/>
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=HTML5&logoColor=white"/> 
</p>

<p align="center">
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=JavaScript&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=Python&logoColor=white">
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=PyTorch&logoColor=white">
</p>
