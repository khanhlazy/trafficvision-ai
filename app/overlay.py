"""OpenCV drawing and output helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import cv2
import numpy as np


COLOR_MAP = {
    "person": (0, 80, 255),
    "car": (255, 120, 0),
    "motorcycle": (255, 0, 255),
    "bus": (0, 180, 255),
    "truck": (0, 255, 255),
    "traffic sign": (0, 255, 120),
    "traffic light": (0, 255, 0),
}


def draw_boxes(image: np.ndarray, predictions: list[dict[str, Any]]) -> np.ndarray:
    output = image.copy()
    for pred in predictions:
        x1, y1, x2, y2 = [int(v) for v in pred["xyxy"]]
        class_name = pred["class_name"]
        color = COLOR_MAP.get(class_name, (220, 220, 220))
        cv2.rectangle(output, (x1, y1), (x2, y2), color, 2)
        label = f"{class_name} {pred['confidence']:.2f}"
        cv2.putText(output, label, (x1, max(18, y1 - 6)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)
    return output


def draw_tracks(image: np.ndarray, predictions: list[dict[str, Any]]) -> np.ndarray:
    output = image.copy()
    for pred in predictions:
        track_id = pred.get("track_id")
        if track_id is None:
            continue
        x1, y1, _, _ = [int(v) for v in pred["xyxy"]]
        cv2.putText(
            output,
            f"ID {track_id}",
            (x1, y1 + 18),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2,
        )
    return output


def draw_vietnamese_warnings(image: np.ndarray, warnings: list[str]) -> np.ndarray:
    output = image.copy()
    y = 28
    for warning in warnings[:4]:
        text = _ascii_warning_text(warning)
        cv2.putText(output, text, (12, y), cv2.FONT_HERSHEY_SIMPLEX, 0.62, (0, 0, 255), 2)
        y += 28
    return output


def draw_warnings(image: np.ndarray, warnings: list[str]) -> np.ndarray:
    return draw_vietnamese_warnings(image, warnings)


def draw_fps(image: np.ndarray, fps: float, processing_time: float | None = None) -> np.ndarray:
    output = image.copy()
    text = f"FPS: {fps:.2f}"
    if processing_time is not None:
        text += f" | Time: {processing_time:.3f}s"
    cv2.putText(output, text, (12, output.shape[0] - 14), cv2.FONT_HERSHEY_SIMPLEX, 0.58, (255, 255, 255), 2)
    return output


def blend_segmentation_mask(image: np.ndarray, mask: np.ndarray | None, alpha: float = 0.35) -> np.ndarray:
    if mask is None:
        return image.copy()
    if mask.ndim == 3:
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    resized_mask = cv2.resize(mask, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_NEAREST)
    color = np.zeros_like(image)
    color[:, :, 1] = resized_mask
    return cv2.addWeighted(image, 1.0 - alpha, color, alpha, 0.0)


def save_image(image: np.ndarray, output_path: str | Path) -> str:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    ok = cv2.imwrite(str(path), image)
    if not ok:
        raise IOError(f"Không thể lưu ảnh kết quả: {path}")
    return str(path)


def create_video_writer(output_path: str | Path, fps: float, frame_size: tuple[int, int]) -> cv2.VideoWriter:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*"mp4v"), fps, frame_size)


def save_video_frame(writer: cv2.VideoWriter, frame: np.ndarray) -> None:
    writer.write(frame)


def _ascii_warning_text(text: str) -> str:
    replacements = {
        "Cảnh báo": "Canh bao",
        "Thông tin": "Thong tin",
        "phát hiện": "phat hien",
        "người đi bộ": "nguoi di bo",
        "phía trước": "phia truoc",
        "phương tiện": "phuong tien",
        "vùng đường chạy": "vung duong chay",
        "biển báo hoặc đèn giao thông": "bien bao hoac den giao thong",
        "không phát hiện rõ làn đường": "khong phat hien ro lan duong",
        "Trạng thái an toàn": "Trang thai an toan",
        "chưa phát hiện nguy cơ rõ ràng": "chua phat hien nguy co ro rang",
    }
    normalized = text
    for source, target in replacements.items():
        normalized = normalized.replace(source, target)
    return normalized[:90]
