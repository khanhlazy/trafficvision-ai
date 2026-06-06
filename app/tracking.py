"""Lightweight object tracking wrapper."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class TrackState:
    track_id: int
    bbox: list[float]
    class_name: str
    missed: int = 0


def box_iou(box_a: list[float], box_b: list[float]) -> float:
    ax1, ay1, ax2, ay2 = box_a
    bx1, by1, bx2, by2 = box_b
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    iw, ih = max(0.0, ix2 - ix1), max(0.0, iy2 - iy1)
    inter = iw * ih
    area_a = max(0.0, ax2 - ax1) * max(0.0, ay2 - ay1)
    area_b = max(0.0, bx2 - bx1) * max(0.0, by2 - by1)
    union = area_a + area_b - inter
    return inter / union if union > 0 else 0.0


class TrafficTracker:
    """Simple IoU tracker used when external tracking is unavailable."""

    def __init__(self, iou_threshold: float = 0.3, max_missed: int = 8) -> None:
        self.iou_threshold = iou_threshold
        self.max_missed = max_missed
        self.next_id = 1
        self.tracks: dict[int, TrackState] = {}
        self.tracking_mode = "IoU fallback"

    def update(self, predictions: list[dict[str, Any]]) -> list[dict[str, Any]]:
        matched_track_ids: set[int] = set()

        for prediction in predictions:
            best_track_id: int | None = None
            best_iou = 0.0
            for track_id, track in self.tracks.items():
                if track_id in matched_track_ids or track.class_name != prediction["class_name"]:
                    continue
                score = box_iou(track.bbox, prediction["xyxy"])
                if score > best_iou:
                    best_iou = score
                    best_track_id = track_id

            if best_track_id is not None and best_iou >= self.iou_threshold:
                track = self.tracks[best_track_id]
                track.bbox = prediction["xyxy"]
                track.missed = 0
                prediction["track_id"] = best_track_id
                matched_track_ids.add(best_track_id)
            else:
                track_id = self.next_id
                self.next_id += 1
                self.tracks[track_id] = TrackState(
                    track_id=track_id,
                    bbox=prediction["xyxy"],
                    class_name=prediction["class_name"],
                )
                prediction["track_id"] = track_id
                matched_track_ids.add(track_id)

        for track_id in list(self.tracks.keys()):
            if track_id not in matched_track_ids:
                self.tracks[track_id].missed += 1
                if self.tracks[track_id].missed > self.max_missed:
                    del self.tracks[track_id]

        return predictions
