"""Rule-based Vietnamese warning engine."""

from __future__ import annotations

from typing import Any


PERSON_CLASSES = {"person"}
VEHICLE_CLASSES = {"car", "motorcycle", "bus", "truck"}
TRAFFIC_CONTROL_CLASSES = {"traffic sign", "traffic light", "stop sign"}

PERSON_WARNING = "Cảnh báo: phát hiện người đi bộ phía trước"
VEHICLE_WARNING = "Cảnh báo: phát hiện phương tiện trong vùng đường chạy"
TRAFFIC_CONTROL_WARNING = "Thông tin: phát hiện biển báo hoặc đèn giao thông"
LANE_WARNING = "Cảnh báo: không phát hiện rõ làn đường"
SAFE_STATUS = "Trạng thái an toàn: chưa phát hiện nguy cơ rõ ràng"


def is_in_center_lower_driving_roi(prediction: dict[str, Any], image_shape: tuple[int, int] | tuple[int, int, int]) -> bool:
    height, width = image_shape[:2]
    center_x = float(prediction["center_x"])
    center_y = float(prediction["center_y"])
    return (width * 0.25 <= center_x <= width * 0.75) and (center_y >= height * 0.52)


def generate_warnings(
    predictions: list[dict[str, Any]],
    *,
    conf_threshold: float,
    image_shape: tuple[int, int] | tuple[int, int, int],
    segmentation_enabled: bool = True,
    road_area_ratio: float | None = None,
    mask_available: bool = True,
) -> list[str]:
    warnings: list[str] = []

    has_person = any(
        pred["class_name"] in PERSON_CLASSES and float(pred["confidence"]) >= conf_threshold for pred in predictions
    )
    if has_person:
        warnings.append(PERSON_WARNING)

    has_vehicle_in_roi = any(
        pred["class_name"] in VEHICLE_CLASSES
        and float(pred["confidence"]) >= conf_threshold
        and is_in_center_lower_driving_roi(pred, image_shape)
        for pred in predictions
    )
    if has_vehicle_in_roi:
        warnings.append(VEHICLE_WARNING)

    has_traffic_control = any(
        pred["class_name"] in TRAFFIC_CONTROL_CLASSES and float(pred["confidence"]) >= conf_threshold
        for pred in predictions
    )
    if has_traffic_control:
        warnings.append(TRAFFIC_CONTROL_WARNING)

    if segmentation_enabled:
        if not mask_available or road_area_ratio is None or road_area_ratio < 0.08:
            warnings.append(LANE_WARNING)

    if not warnings:
        warnings.append(SAFE_STATUS)
    return warnings
