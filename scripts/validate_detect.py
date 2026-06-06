"""Validate a YOLO detector and save metrics."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cli_utils import configure_utf8_stdio
from app.logging_utils import make_timestamp

configure_utf8_stdio()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate YOLO traffic detector.")
    parser.add_argument("--model", default="models/weights/best.pt")
    parser.add_argument("--data", default="datasets/bdd_custom_detect.yaml")
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--output-dir", default="outputs/metrics")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        from ultralytics import YOLO
    except Exception as exc:
        raise SystemExit(f"Không thể import Ultralytics: {exc}")

    model_path = ROOT / args.model
    model = YOLO(str(model_path if model_path.exists() else args.model))
    results = model.val(data=args.data, imgsz=args.imgsz)
    metrics = getattr(results, "results_dict", {}) or {}

    output_dir = ROOT / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = make_timestamp()
    json_path = output_dir / f"detect_metrics_{timestamp}.json"
    csv_path = output_dir / f"detect_metrics_{timestamp}.csv"
    json_path.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    with csv_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["metric", "value"])
        for key, value in metrics.items():
            writer.writerow([key, value])
    print(f"Đã lưu metrics: {json_path}")
    print(f"Đã lưu CSV: {csv_path}")


if __name__ == "__main__":
    main()
