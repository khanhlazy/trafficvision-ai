"""Pydantic schemas used by API and logging layers."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class Prediction(BaseModel):
    class_name: str
    class_id: int
    confidence: float = Field(ge=0.0, le=1.0)
    xyxy: list[float] = Field(min_length=4, max_length=4)
    area: float = Field(ge=0.0)
    center_x: float
    center_y: float
    track_id: int | None = None


class WarningMessage(BaseModel):
    message: str
    level: Literal["info", "warning", "safe"] = "info"
    source: str = "rule_engine"


class ModelInfo(BaseModel):
    detector_model: str
    detector_mode: str
    segmentation_mode: str
    tracking_mode: str


class SegmentationInfo(BaseModel):
    segmentation_mode: str
    road_area_ratio: float | None = None
    is_fallback: bool = True
    model_path: str | None = None
    message: str | None = None


class PipelineResult(BaseModel):
    status: str = "ok"
    timestamp: str
    input_path: str | None = None
    output_path: str | None = None
    model_name: str
    conf_threshold: float
    predictions: list[Prediction]
    warnings: list[str]
    fps: float
    processing_time: float
    segmentation_mode: str
    road_area_ratio: float | None = None
    model_info: ModelInfo
    segmentation_info: SegmentationInfo | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


class APIResponse(BaseModel):
    status: str
    predictions: list[Prediction] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    processing_time: float = 0.0
    model_info: ModelInfo
    segmentation_info: SegmentationInfo | None = None
    message: str | None = None
