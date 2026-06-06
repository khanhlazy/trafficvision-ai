"""Run image prediction from the command line."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cli_utils import configure_utf8_stdio
from app.inference import TrafficAIPipeline
from app.logging_utils import sanitize_for_json

configure_utf8_stdio()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Predict a traffic image.")
    parser.add_argument("image", help="Input image path.")
    parser.add_argument("--conf", type=float, default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--no-save", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    pipeline = TrafficAIPipeline()
    result = pipeline.process_image(args.image, conf=args.conf, save_output=not args.no_save, output_path=args.output)
    print(json.dumps(sanitize_for_json(result), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
