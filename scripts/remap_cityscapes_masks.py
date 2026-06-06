"""Remap Cityscapes label masks to binary road/drivable masks."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image
from tqdm import tqdm

from cli_utils import configure_utf8_stdio

configure_utf8_stdio()


ROAD_LABEL_IDS = {7}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Remap Cityscapes masks to binary road masks.")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--road-label-ids", type=int, nargs="*", default=sorted(ROAD_LABEL_IDS))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    road_ids = set(args.road_label_ids)
    mask_paths = sorted(input_dir.rglob("*.png"))
    for mask_path in tqdm(mask_paths, desc="Remap masks"):
        mask = np.array(Image.open(mask_path))
        binary = np.where(np.isin(mask, list(road_ids)), 255, 0).astype(np.uint8)
        target = output_dir / mask_path.relative_to(input_dir)
        target.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(binary).save(target)
    print(f"Đã remap {len(mask_paths)} mask vào {output_dir}")


if __name__ == "__main__":
    main()
