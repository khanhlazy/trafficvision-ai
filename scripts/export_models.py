"""Export YOLO weights to ONNX and optionally TensorRT."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cli_utils import configure_utf8_stdio

configure_utf8_stdio()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export detector model.")
    parser.add_argument("--model", default="models/weights/best.pt")
    parser.add_argument("--format", default="onnx", choices=["onnx", "engine"])
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--output-dir", default="models/exported")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        from ultralytics import YOLO
    except Exception as exc:
        raise SystemExit(f"Không thể import Ultralytics: {exc}")

    model_path = ROOT / args.model
    if not model_path.exists():
        raise SystemExit(f"Không tìm thấy model: {model_path}. Hãy đặt best.pt vào models/weights/.")

    if args.format == "engine" and shutil.which("trtexec") is None:
        print("TensorRT/trtexec chưa khả dụng. Hãy cài NVIDIA TensorRT nếu muốn export .engine.")
        print("Tiếp tục export ONNX để dùng cho kiểm thử CPU/GPU thông thường.")
        args.format = "onnx"

    model = YOLO(str(model_path))
    exported_path = model.export(format=args.format, imgsz=args.imgsz)
    output_dir = ROOT / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    exported = Path(exported_path)
    target = output_dir / exported.name
    if exported.exists() and exported.resolve() != target.resolve():
        shutil.copy2(exported, target)
    print(f"Đã export model: {target if target.exists() else exported_path}")


if __name__ == "__main__":
    main()
