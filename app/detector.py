"""Traffic object detector using Ultralytics YOLO with an offline-safe fallback."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from app.config import BASE_DIR, Settings, get_settings


TARGET_CLASS_MAP = {
    "person": "person",
    "car": "car",
    "motorcycle": "motorcycle",
    "motorbike": "motorcycle",
    "bus": "bus",
    "truck": "truck",
    "traffic light": "traffic light",
    "traffic sign": "traffic sign",
    "stop sign": "traffic sign",
}


class TrafficDetector:
    """YOLO detector wrapper that never crashes when weights are unavailable."""

    def __init__(self, settings: Settings | None = None, model_path: str | Path | None = None) -> None:
        self.settings = settings or get_settings()
        self.requested_model_path = Path(model_path) if model_path else self.settings.det_model_path
        self.model: Any | None = None
        self.model_name = "offline_demo_detector"
        self.model_mode = "fallback"
        self.names: dict[int, str] = {}
        self.error_message: str | None = None
        self._load_model()

    def _candidate_paths(self) -> list[Path | str]:
        candidates: list[Path | str] = []
        if self.requested_model_path:
            candidates.append(self.requested_model_path)
        weights_dir = BASE_DIR / "models" / "weights"
        fallback_names = [
            self.settings.model_fallback_name,
            "yolo11n.pt",
            "yolov8n.pt",
        ]
        for name in dict.fromkeys(fallback_names):
            candidates.append(weights_dir / name)
            if self.settings.allow_model_download:
                candidates.append(name)
        return candidates

    def _load_model(self) -> None:
        loadable_candidates: list[Path | str] = []
        for candidate in self._candidate_paths():
            if isinstance(candidate, str):
                loadable_candidates.append(candidate)
            elif Path(candidate).exists():
                loadable_candidates.append(candidate)

        if not loadable_candidates:
            self.error_message = "Không tìm thấy weight YOLO local; detector đang chạy fallback offline."
            return

        try:
            from ultralytics import YOLO
        except Exception as exc:  # pragma: no cover - depends on optional package
            self.error_message = f"Ultralytics chưa khả dụng: {exc}"
            return

        for candidate in loadable_candidates:
            try:
                self.model = YOLO(str(candidate))
                self.model_name = str(candidate)
                suffix = Path(str(candidate)).suffix.lower()
                self.model_mode = "ONNX" if suffix == ".onnx" else "PyTorch"
                self.names = getattr(self.model, "names", {}) or {}
                return
            except Exception as exc:  # pragma: no cover - model runtime dependent
                self.error_message = f"Không thể tải mô hình {candidate}: {exc}"
                self.model = None

    def detect_image(self, image: np.ndarray, conf: float | None = None) -> list[dict[str, Any]]:
        return self.detect_frame(image, conf)

    def detect_frame(self, frame: np.ndarray, conf: float | None = None) -> list[dict[str, Any]]:
        if frame is None or frame.size == 0:
            raise ValueError("Ảnh hoặc khung hình không hợp lệ.")
        if self.model is None:
            return []
        threshold = conf if conf is not None else self.settings.default_conf
        try:
            results = self.model(frame, conf=threshold, verbose=False)
            return self.parse_results(results)
        except Exception as exc:
            self.error_message = f"Lỗi suy luận YOLO: {exc}"
            return []

    def get_model_info(self) -> dict[str, Any]:
        return {
            "detector_model": self.model_name,
            "detector_mode": self.model_mode,
            "requested_model_path": str(self.requested_model_path),
            "fallback_name": self.settings.model_fallback_name,
            "is_fallback": self.model is None or self.model_mode == "fallback",
            "message": self.error_message,
        }

    def parse_results(self, results: Any) -> list[dict[str, Any]]:
        predictions: list[dict[str, Any]] = []
        if results is None:
            return predictions

        result_list = results if isinstance(results, (list, tuple)) else [results]
        for result in result_list:
            boxes = getattr(result, "boxes", None)
            names = getattr(result, "names", None) or self.names
            if boxes is None:
                continue
            for box in boxes:
                parsed = self._parse_box(box, names)
                if parsed is not None:
                    predictions.append(parsed)
        return predictions

    def _parse_box(self, box: Any, names: dict[int, str]) -> dict[str, Any] | None:
        try:
            xyxy = self._to_list(box.xyxy[0])
            confidence = float(self._to_scalar(box.conf[0]))
            class_id = int(self._to_scalar(box.cls[0]))
        except Exception:
            return None

        raw_name = str(names.get(class_id, class_id)).lower()
        class_name = TARGET_CLASS_MAP.get(raw_name)
        if class_name is None:
            return None

        x1, y1, x2, y2 = [float(v) for v in xyxy]
        area = max(0.0, x2 - x1) * max(0.0, y2 - y1)
        return {
            "class_name": class_name,
            "class_id": class_id,
            "confidence": confidence,
            "xyxy": [x1, y1, x2, y2],
            "area": area,
            "center_x": (x1 + x2) / 2.0,
            "center_y": (y1 + y2) / 2.0,
            "track_id": None,
        }

    @staticmethod
    def _to_scalar(value: Any) -> float:
        if hasattr(value, "item"):
            return float(value.item())
        return float(value)

    @staticmethod
    def _to_list(value: Any) -> list[float]:
        if hasattr(value, "detach"):
            value = value.detach().cpu().numpy()
        if hasattr(value, "tolist"):
            return list(value.tolist())
        return list(value)
