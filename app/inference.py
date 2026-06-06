"""End-to-end OpenCV inference pipeline."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import cv2
import numpy as np

from app.config import Settings, get_settings
from app.detector import TrafficDetector
from app.logging_utils import make_timestamp, save_run_log
from app.logic import generate_warnings
from app.overlay import blend_segmentation_mask, create_video_writer, draw_boxes, draw_fps, draw_tracks, draw_warnings, save_image
from app.segmenter import LaneRoadSegmenter
from app.tracking import TrafficTracker


class TrafficAIPipeline:
    """Modular pipeline for image, video, and webcam traffic AI inference."""

    def __init__(
        self,
        settings: Settings | None = None,
        detector: TrafficDetector | None = None,
        segmenter: LaneRoadSegmenter | None = None,
        tracker: TrafficTracker | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.detector = detector or TrafficDetector(self.settings)
        self.segmenter = segmenter or LaneRoadSegmenter(self.settings)
        self.tracker = tracker or TrafficTracker()

    def process_image(
        self,
        image_path_or_array: str | Path | np.ndarray,
        conf: float | None = None,
        *,
        save_output: bool = True,
        output_path: str | Path | None = None,
    ) -> dict[str, Any]:
        frame, input_path = self._read_image(image_path_or_array)
        threshold = conf if conf is not None else self.settings.default_conf
        started = time.perf_counter()

        predictions = self.detector.detect_frame(frame, threshold)

        mask = None
        road_area_ratio = None
        segmentation_mode = "Tắt phân vùng"
        segmentation_is_fallback = False
        if self.settings.enable_segmentation:
            segmentation = self.segmenter.segment_frame(frame)
            mask = segmentation["mask"]
            road_area_ratio = segmentation["road_area_ratio"]
            segmentation_mode = segmentation["segmentation_mode"]
            segmentation_is_fallback = bool(segmentation.get("is_fallback", False))

        if self.settings.enable_tracking:
            predictions = self.tracker.update(predictions)

        processing_time = time.perf_counter() - started
        fps = 1.0 / processing_time if processing_time > 0 else 0.0
        warnings = generate_warnings(
            predictions,
            conf_threshold=threshold,
            image_shape=frame.shape,
            segmentation_enabled=self.settings.enable_segmentation,
            road_area_ratio=road_area_ratio,
            mask_available=mask is not None,
        )

        annotated = self._draw_result(frame, predictions, warnings, fps, processing_time, mask)
        saved_output_path = None
        timestamp = make_timestamp()
        if save_output:
            target = Path(output_path) if output_path else self.settings.images_dir / f"result_{timestamp}.jpg"
            saved_output_path = save_image(annotated, target)

        result = {
            "status": "ok",
            "timestamp": timestamp,
            "input_path": str(input_path) if input_path else None,
            "output_path": saved_output_path,
            "model_name": self.detector.model_name,
            "conf_threshold": threshold,
            "predictions": predictions,
            "warnings": warnings,
            "fps": fps,
            "processing_time": processing_time,
            "segmentation_mode": segmentation_mode,
            "road_area_ratio": road_area_ratio,
            "model_info": self.model_info(segmentation_mode),
            "segmentation_info": self.segmentation_info(segmentation_mode, road_area_ratio, segmentation_is_fallback),
            "annotated_image": annotated,
        }
        if self.settings.save_logs:
            result["log_path"] = save_run_log(result, self.settings)
        return result

    def process_video(
        self,
        video_path: str | Path,
        output_path: str | Path | None = None,
        conf: float | None = None,
        max_frames: int | None = None,
    ) -> dict[str, Any]:
        capture = cv2.VideoCapture(str(video_path))
        if not capture.isOpened():
            raise ValueError(f"Không thể mở video: {video_path}")

        fps_source = capture.get(cv2.CAP_PROP_FPS) or 25.0
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH) or 640)
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT) or 480)
        timestamp = make_timestamp()
        target = Path(output_path) if output_path else self.settings.videos_dir / f"result_{timestamp}.mp4"
        target.parent.mkdir(parents=True, exist_ok=True)
        writer = create_video_writer(target, fps_source, (width, height))

        frame_count = 0
        all_predictions: list[dict[str, Any]] = []
        all_warnings: list[str] = []
        started = time.perf_counter()
        threshold = conf if conf is not None else self.settings.default_conf
        segmentation_mode = "Tắt phân vùng"
        road_area_ratio = None
        segmentation_is_fallback = False

        while True:
            ok, frame = capture.read()
            if not ok:
                break
            frame_result = self._process_frame(frame, threshold)
            writer.write(frame_result["annotated_image"])
            all_predictions.extend(frame_result["predictions"])
            all_warnings = frame_result["warnings"]
            segmentation_mode = frame_result["segmentation_mode"]
            road_area_ratio = frame_result["road_area_ratio"]
            segmentation_is_fallback = frame_result["segmentation_is_fallback"]
            frame_count += 1
            if max_frames is not None and frame_count >= max_frames:
                break

        capture.release()
        writer.release()
        processing_time = time.perf_counter() - started
        fps = frame_count / processing_time if processing_time > 0 else 0.0
        result = {
            "status": "ok",
            "timestamp": timestamp,
            "input_path": str(video_path),
            "output_path": str(target),
            "model_name": self.detector.model_name,
            "conf_threshold": threshold,
            "predictions": all_predictions[-100:],
            "warnings": all_warnings,
            "fps": fps,
            "processing_time": processing_time,
            "frame_count": frame_count,
            "segmentation_mode": segmentation_mode,
            "road_area_ratio": road_area_ratio,
            "model_info": self.model_info(segmentation_mode),
            "segmentation_info": self.segmentation_info(segmentation_mode, road_area_ratio, segmentation_is_fallback),
        }
        if self.settings.save_logs:
            result["log_path"] = save_run_log(result, self.settings, prefix="video_inference")
        return result

    def process_webcam(self, camera_id: int = 0, max_frames: int | None = None) -> dict[str, Any]:
        capture = cv2.VideoCapture(camera_id)
        if not capture.isOpened():
            raise ValueError(f"Không thể mở webcam ID {camera_id}")

        fps_source = capture.get(cv2.CAP_PROP_FPS) or 25.0
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH) or 640)
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT) or 480)
        timestamp = make_timestamp()
        target = self.settings.videos_dir / f"webcam_{timestamp}.mp4"
        target.parent.mkdir(parents=True, exist_ok=True)
        writer = create_video_writer(target, fps_source, (width, height))

        frame_count = 0
        warnings: list[str] = []
        segmentation_mode = "Tắt phân vùng"
        road_area_ratio = None
        segmentation_is_fallback = False
        started = time.perf_counter()
        while True:
            ok, frame = capture.read()
            if not ok:
                break
            frame_result = self._process_frame(frame, self.settings.default_conf)
            writer.write(frame_result["annotated_image"])
            warnings = frame_result["warnings"]
            segmentation_mode = frame_result["segmentation_mode"]
            road_area_ratio = frame_result["road_area_ratio"]
            segmentation_is_fallback = frame_result["segmentation_is_fallback"]
            frame_count += 1
            if max_frames is not None and frame_count >= max_frames:
                break

        capture.release()
        writer.release()
        processing_time = time.perf_counter() - started
        fps = frame_count / processing_time if processing_time > 0 else 0.0
        result = {
            "status": "ok",
            "timestamp": timestamp,
            "input_path": f"webcam:{camera_id}",
            "output_path": str(target),
            "model_name": self.detector.model_name,
            "conf_threshold": self.settings.default_conf,
            "predictions": [],
            "warnings": warnings,
            "fps": fps,
            "processing_time": processing_time,
            "frame_count": frame_count,
            "segmentation_mode": segmentation_mode,
            "road_area_ratio": road_area_ratio,
            "model_info": self.model_info(segmentation_mode),
            "segmentation_info": self.segmentation_info(segmentation_mode, road_area_ratio, segmentation_is_fallback),
        }
        if self.settings.save_logs:
            result["log_path"] = save_run_log(result, self.settings, prefix="webcam_inference")
        return result

    def _process_frame(self, frame: np.ndarray, threshold: float) -> dict[str, Any]:
        started = time.perf_counter()
        predictions = self.detector.detect_frame(frame, threshold)
        mask = None
        road_area_ratio = None
        segmentation_mode = "Tắt phân vùng"
        segmentation_is_fallback = False
        if self.settings.enable_segmentation:
            segmentation = self.segmenter.segment_frame(frame)
            mask = segmentation["mask"]
            road_area_ratio = segmentation["road_area_ratio"]
            segmentation_mode = segmentation["segmentation_mode"]
            segmentation_is_fallback = bool(segmentation.get("is_fallback", False))
        if self.settings.enable_tracking:
            predictions = self.tracker.update(predictions)
        processing_time = time.perf_counter() - started
        fps = 1.0 / processing_time if processing_time > 0 else 0.0
        warnings = generate_warnings(
            predictions,
            conf_threshold=threshold,
            image_shape=frame.shape,
            segmentation_enabled=self.settings.enable_segmentation,
            road_area_ratio=road_area_ratio,
            mask_available=mask is not None,
        )
        return {
            "predictions": predictions,
            "warnings": warnings,
            "fps": fps,
            "processing_time": processing_time,
            "segmentation_mode": segmentation_mode,
            "road_area_ratio": road_area_ratio,
            "segmentation_is_fallback": segmentation_is_fallback,
            "annotated_image": self._draw_result(frame, predictions, warnings, fps, processing_time, mask),
        }

    def _draw_result(
        self,
        frame: np.ndarray,
        predictions: list[dict[str, Any]],
        warnings: list[str],
        fps: float,
        processing_time: float,
        mask: np.ndarray | None,
    ) -> np.ndarray:
        annotated = blend_segmentation_mask(frame, mask)
        annotated = draw_boxes(annotated, predictions)
        if self.settings.enable_tracking:
            annotated = draw_tracks(annotated, predictions)
        annotated = draw_warnings(annotated, warnings)
        annotated = draw_fps(annotated, fps, processing_time)
        return annotated

    def _read_image(self, image_path_or_array: str | Path | np.ndarray) -> tuple[np.ndarray, Path | None]:
        if isinstance(image_path_or_array, np.ndarray):
            if image_path_or_array.ndim not in {2, 3}:
                raise ValueError("Mảng ảnh không hợp lệ.")
            return image_path_or_array.copy(), None
        path = Path(image_path_or_array)
        frame = cv2.imread(str(path))
        if frame is None:
            raise ValueError(f"Không thể đọc ảnh: {path}")
        return frame, path

    def model_info(self, segmentation_mode: str | None = None) -> dict[str, str]:
        detector_info = self.detector.get_model_info()
        return {
            "detector_model": detector_info["detector_model"],
            "detector_mode": detector_info["detector_mode"],
            "segmentation_mode": segmentation_mode or self.segmenter.segmentation_mode,
            "tracking_mode": self.tracker.tracking_mode if self.settings.enable_tracking else "Tắt tracking",
        }

    def segmentation_info(
        self,
        segmentation_mode: str | None = None,
        road_area_ratio: float | None = None,
        is_fallback: bool | None = None,
    ) -> dict[str, Any]:
        segmenter_info = self.segmenter.get_segmenter_info()
        return {
            "segmentation_mode": segmentation_mode or segmenter_info["segmentation_mode"],
            "road_area_ratio": road_area_ratio,
            "is_fallback": segmenter_info["is_fallback"] if is_fallback is None else is_fallback,
            "model_path": segmenter_info["model_path"],
            "message": segmenter_info["message"],
        }
