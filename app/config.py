"""Application configuration helpers."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DET_MODEL_PATH = BASE_DIR / "models" / "weights" / "best.pt"
DEFAULT_SEG_MODEL_PATH = BASE_DIR / "models" / "weights" / "deeplabv3plus_road.pth"
DEFAULT_OUTPUT_DIR = BASE_DIR / "outputs"
DEFAULT_CONF = 0.35
DEFAULT_ENABLE_SEGMENTATION = True
DEFAULT_ENABLE_TRACKING = True
DEFAULT_SAVE_LOGS = True
DEFAULT_ALLOW_MODEL_DOWNLOAD = False
DEFAULT_MODEL_FALLBACK_NAME = "yolo11n.pt"
DEFAULT_STREAMLIT_UPLOAD_LIMIT_NOTE = "Nếu video quá lớn, hãy dùng script predict_video.py để xử lý ổn định hơn."
DEFAULT_API_TITLE = "TrafficVision AI API"


def _as_bool(value: str | bool | None, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return value.strip().lower() in {"1", "true", "yes", "y", "on", "bật", "bat"}


def _as_float(value: str | float | None, default: float) -> float:
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


@dataclass(slots=True)
class Settings:
    det_model_path: Path = DEFAULT_DET_MODEL_PATH
    seg_model_path: Path = DEFAULT_SEG_MODEL_PATH
    output_dir: Path = DEFAULT_OUTPUT_DIR
    default_conf: float = DEFAULT_CONF
    enable_segmentation: bool = DEFAULT_ENABLE_SEGMENTATION
    enable_tracking: bool = DEFAULT_ENABLE_TRACKING
    save_logs: bool = DEFAULT_SAVE_LOGS
    allow_model_download: bool = DEFAULT_ALLOW_MODEL_DOWNLOAD
    model_fallback_name: str = DEFAULT_MODEL_FALLBACK_NAME
    streamlit_upload_limit_note: str = DEFAULT_STREAMLIT_UPLOAD_LIMIT_NOTE
    api_title: str = DEFAULT_API_TITLE

    @property
    def images_dir(self) -> Path:
        return self.output_dir / "images"

    @property
    def videos_dir(self) -> Path:
        return self.output_dir / "videos"

    @property
    def logs_dir(self) -> Path:
        return self.output_dir / "logs"

    @property
    def metrics_dir(self) -> Path:
        return self.output_dir / "metrics"

    @property
    def reports_dir(self) -> Path:
        return self.output_dir / "reports"

    def ensure_directories(self) -> None:
        for path in [
            self.output_dir,
            self.images_dir,
            self.videos_dir,
            self.logs_dir,
            self.metrics_dir,
            self.reports_dir,
        ]:
            path.mkdir(parents=True, exist_ok=True)


def get_settings() -> Settings:
    settings = Settings(
        det_model_path=Path(os.getenv("DET_MODEL_PATH", str(DEFAULT_DET_MODEL_PATH))),
        seg_model_path=Path(os.getenv("SEG_MODEL_PATH", str(DEFAULT_SEG_MODEL_PATH))),
        output_dir=Path(os.getenv("OUTPUT_DIR", str(DEFAULT_OUTPUT_DIR))),
        default_conf=_as_float(os.getenv("DEFAULT_CONF"), DEFAULT_CONF),
        enable_segmentation=_as_bool(os.getenv("ENABLE_SEGMENTATION"), DEFAULT_ENABLE_SEGMENTATION),
        enable_tracking=_as_bool(os.getenv("ENABLE_TRACKING"), DEFAULT_ENABLE_TRACKING),
        save_logs=_as_bool(os.getenv("SAVE_LOGS"), DEFAULT_SAVE_LOGS),
        allow_model_download=_as_bool(os.getenv("ALLOW_MODEL_DOWNLOAD"), DEFAULT_ALLOW_MODEL_DOWNLOAD),
        model_fallback_name=os.getenv("MODEL_FALLBACK_NAME", DEFAULT_MODEL_FALLBACK_NAME),
        streamlit_upload_limit_note=os.getenv("STREAMLIT_UPLOAD_LIMIT_NOTE", DEFAULT_STREAMLIT_UPLOAD_LIMIT_NOTE),
        api_title=os.getenv("API_TITLE", DEFAULT_API_TITLE),
    )
    settings.ensure_directories()
    return settings
