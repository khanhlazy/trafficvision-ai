"""Convert a COCO-like detection annotation file to YOLO format."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from cli_utils import configure_utf8_stdio

configure_utf8_stdio()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert COCO-like annotations to YOLO labels.")
    parser.add_argument("--input-json", required=True)
    parser.add_argument("--output-labels", required=True)
    parser.add_argument("--classes", nargs="+", default=["person", "car", "motorcycle", "bus", "truck", "traffic light", "traffic sign"])
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source = Path(args.input_json)
    output_dir = Path(args.output_labels)
    output_dir.mkdir(parents=True, exist_ok=True)
    data = json.loads(source.read_text(encoding="utf-8"))
    images = {item["id"]: item for item in data.get("images", [])}
    categories = {item["id"]: item["name"] for item in data.get("categories", [])}
    class_to_id = {name: idx for idx, name in enumerate(args.classes)}
    label_lines: dict[str, list[str]] = {}

    for ann in data.get("annotations", []):
        image = images.get(ann.get("image_id"))
        if not image:
            continue
        category_name = categories.get(ann.get("category_id"))
        if category_name not in class_to_id:
            continue
        width, height = float(image["width"]), float(image["height"])
        x, y, w, h = [float(v) for v in ann["bbox"]]
        x_center = (x + w / 2.0) / width
        y_center = (y + h / 2.0) / height
        line = f"{class_to_id[category_name]} {x_center:.6f} {y_center:.6f} {w / width:.6f} {h / height:.6f}"
        stem = Path(image["file_name"]).stem
        label_lines.setdefault(stem, []).append(line)

    for stem, lines in label_lines.items():
        (output_dir / f"{stem}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Đã chuyển đổi {len(label_lines)} file nhãn YOLO vào {output_dir}")


if __name__ == "__main__":
    main()
