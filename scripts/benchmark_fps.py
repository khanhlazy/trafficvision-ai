"""Benchmark FPS and latency for image pipeline."""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cli_utils import configure_utf8_stdio
from app.inference import TrafficAIPipeline
from app.logging_utils import make_timestamp

configure_utf8_stdio()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark pipeline FPS.")
    parser.add_argument("--image", default=None)
    parser.add_argument("--runs", type=int, default=20)
    parser.add_argument("--output-dir", default="outputs/metrics")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.image:
        frame = cv2.imread(args.image)
        if frame is None:
            raise SystemExit(f"Không thể đọc ảnh benchmark: {args.image}")
    else:
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.rectangle(frame, (170, 260), (470, 479), (60, 60, 60), -1)

    pipeline = TrafficAIPipeline()
    latencies = []
    for _ in range(args.runs):
        started = time.perf_counter()
        pipeline.process_image(frame, save_output=False)
        latencies.append(time.perf_counter() - started)

    avg_latency = sum(latencies) / len(latencies)
    metrics = {
        "timestamp": make_timestamp(),
        "runs": args.runs,
        "avg_latency_seconds": avg_latency,
        "avg_fps": 1.0 / avg_latency if avg_latency > 0 else 0.0,
        "min_latency_seconds": min(latencies),
        "max_latency_seconds": max(latencies),
    }
    output_dir = ROOT / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"benchmark_{metrics['timestamp']}.json"
    csv_path = output_dir / f"benchmark_{metrics['timestamp']}.csv"
    json_path.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    with csv_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(metrics.keys()))
        writer.writeheader()
        writer.writerow(metrics)
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
