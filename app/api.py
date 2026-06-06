"""FastAPI service for image prediction."""

from __future__ import annotations

import cv2
import numpy as np
from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from app.config import get_settings
from app.inference import TrafficAIPipeline


settings = get_settings()
pipeline = TrafficAIPipeline(settings=settings)

app = FastAPI(
    title=settings.api_title,
    description="API phát hiện phương tiện, biển báo và phân vùng làn đường.",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "message": "API sẵn sàng",
        "model_info": pipeline.model_info(),
        "segmentation_info": pipeline.segmentation_info(),
    }


@app.post("/predict/image")
async def predict_image(file: UploadFile = File(...), conf: float = Form(settings.default_conf)) -> dict:
    try:
        content = await file.read()
        image_array = np.frombuffer(content, dtype=np.uint8)
        frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        if frame is None:
            raise ValueError("Tệp tải lên không phải ảnh hợp lệ.")
        result = pipeline.process_image(frame, conf=conf, save_output=True)
        return {
            "status": "ok",
            "predictions": result["predictions"],
            "warnings": result["warnings"],
            "processing_time": result["processing_time"],
            "model_info": result["model_info"],
            "segmentation_info": result["segmentation_info"],
            "output_path": result.get("output_path"),
            "message": "Dự đoán ảnh thành công",
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Lỗi xử lý ảnh: {exc}") from exc


@app.post("/predict/video")
async def predict_video_metadata(file: UploadFile = File(...)) -> dict:
    return {
        "status": "ok",
        "message": "API đã nhận metadata video. Xử lý video đầy đủ nên chạy qua giao diện hoặc script CLI.",
        "filename": file.filename,
        "content_type": file.content_type,
        "model_info": pipeline.model_info(),
        "segmentation_info": pipeline.segmentation_info(),
    }
