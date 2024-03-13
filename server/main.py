from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
import os
from model import stream_detected_frames, get_signal, generate_frames

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def video_streaming(file_path):
    return stream_detected_frames(file_path)

# 파일 스트리밍 함수
@app.get("/stream")
async def stream_video():
    try:
        # 동영상 파일 경로
        file_path = './videoStorage/video.mp4'
        # 동영상 파일이 존재하는지 확인
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")

        frame = video_streaming(file_path)
        # 객체 탐지가 수행된 프레임을 클라이언트로 스트리밍
        return StreamingResponse(frame, media_type="multipart/x-mixed-replace; boundary=frame")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# HTML 페이지를 반환하는 엔드포인트
@app.get("/signal")
async def get():
    content = get_signal()
    return content
    
@app.get("/get_person")
async def stream_person():
    return StreamingResponse(generate_frames(),
                             media_type="multipart/x-mixed-replace; boundary=frame")