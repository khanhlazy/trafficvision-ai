"""Train YOLO detector for traffic classes."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cli_utils import configure_utf8_stdio

configure_utf8_stdio()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train YOLO traffic detector.")
    parser.add_argument("--data", default="datasets/bdd_custom_detect.yaml", help="YOLO data yaml path.")
    parser.add_argument("--model", default="yolo11s.pt", help="Base YOLO model, for example yolo11s.pt.")
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=8)
    parser.add_argument("--project", default="runs/detect")
    parser.add_argument("--name", default="traffic_yolo")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        from ultralytics import YOLO
    except Exception as exc:
        raise SystemExit(f"Không thể import Ultralytics. Hãy chạy `pip install -r requirements.txt`. Chi tiết: {exc}")

    model = YOLO(args.model)
    model.train(
        data=args.data,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        project=args.project,
        name=args.name,
    )


if __name__ == "__main__":
    main()
