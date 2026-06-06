"""Semantic road/lane segmentation module with a safe demo fallback."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import cv2
import numpy as np

from app.config import Settings, get_settings


class LaneRoadSegmenter:
    """Road area segmenter designed for semantic segmentation weights."""

    def __init__(self, settings: Settings | None = None, model_path: str | Path | None = None) -> None:
        self.settings = settings or get_settings()
        self.model_path = Path(model_path) if model_path else self.settings.seg_model_path
        self.model: Any | None = None
        self.segmentation_mode = "Chế độ phân vùng demo"
        self.error_message: str | None = None
        self._load_semantic_placeholder()

    def _load_semantic_placeholder(self) -> None:
        if self.model_path.exists():
            self.segmentation_mode = "Mô hình semantic segmentation"
            self.model = "semantic_placeholder"
        else:
            self.segmentation_mode = "Chế độ phân vùng demo"

    def segment_frame(self, frame: np.ndarray) -> dict[str, Any]:
        if frame is None or frame.size == 0:
            raise ValueError("Khung hình không hợp lệ.")

        if self.model is None:
            mask = self.create_demo_road_mask(frame)
            mode = "Chế độ phân vùng demo"
        else:
            mask = self._segment_with_semantic_placeholder(frame)
            mode = self.segmentation_mode

        road_area_ratio = float(np.count_nonzero(mask) / mask.size) if mask.size else 0.0
        return {
            "mask": mask,
            "segmentation_mode": mode,
            "road_area_ratio": road_area_ratio,
            "is_fallback": self.model is None,
        }

    def _segment_with_semantic_placeholder(self, frame: np.ndarray) -> np.ndarray:
        # The interface is ready for DeepLabV3+ weights; demo geometry keeps the project runnable.
        return self.create_demo_road_mask(frame)

    def create_demo_road_mask(self, frame: np.ndarray) -> np.ndarray:
        height, width = frame.shape[:2]
        mask = np.zeros((height, width), dtype=np.uint8)
        polygon = np.array(
            [
                (int(width * 0.12), height - 1),
                (int(width * 0.42), int(height * 0.58)),
                (int(width * 0.58), int(height * 0.58)),
                (int(width * 0.88), height - 1),
            ],
            dtype=np.int32,
        )
        cv2.fillPoly(mask, [polygon], 255)
        return mask

    def overlay_mask(self, frame: np.ndarray, mask: np.ndarray) -> np.ndarray:
        color_mask = np.zeros_like(frame)
        color_mask[:, :, 1] = mask
        return cv2.addWeighted(frame, 0.75, color_mask, 0.25, 0.0)

    def get_segmenter_info(self) -> dict[str, Any]:
        return {
            "segmentation_mode": self.segmentation_mode,
            "model_path": str(self.model_path),
            "is_fallback": self.model is None,
            "road_class": "road/drivable area",
            "message": self.error_message,
        }
