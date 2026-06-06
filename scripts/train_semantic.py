"""Prepare a semantic segmentation training plan for road/lane masks."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cli_utils import configure_utf8_stdio
from app.logging_utils import make_timestamp

configure_utf8_stdio()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create semantic segmentation training plan.")
    parser.add_argument("--data", default="datasets/cityscapes_semantic.yaml")
    parser.add_argument("--architecture", default="deeplabv3plus")
    parser.add_argument("--epochs", type=int, default=40)
    parser.add_argument("--imgsz", type=int, default=512)
    parser.add_argument("--batch", type=int, default=4)
    parser.add_argument("--output", default="outputs/metrics/semantic_training_plan.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    plan = {
        "timestamp": make_timestamp(),
        "architecture": args.architecture,
        "dataset_config": args.data,
        "epochs": args.epochs,
        "imgsz": args.imgsz,
        "batch": args.batch,
        "note": (
            "Module runtime đã thiết kế theo semantic segmentation. "
            "Khi có mask Cityscapes/BDD100K đã remap, thay phần placeholder bằng trainer PyTorch DeepLabV3+."
        ),
        "expected_weights": "models/weights/deeplabv3plus_road.pth",
    }
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Đã tạo kế hoạch huấn luyện semantic segmentation: {output}")


if __name__ == "__main__":
    main()
