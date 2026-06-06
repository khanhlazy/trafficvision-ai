"""Create a small synthetic traffic image for smoke tests and demos."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np

from cli_utils import configure_utf8_stdio

configure_utf8_stdio()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create synthetic sample data.")
    parser.add_argument("--output", default="datasets/samples/sample_road.jpg")
    parser.add_argument("--video-output", default="datasets/samples/sample_video.mp4")
    parser.add_argument("--frames", type=int, default=24)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    image = create_synthetic_frame(0)
    cv2.imwrite(str(output), image)
    print(f"Đã tạo ảnh mẫu: {output}")

    video_output = Path(args.video_output)
    video_output.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(str(video_output), cv2.VideoWriter_fourcc(*"mp4v"), 8.0, (640, 480))
    for frame_index in range(args.frames):
        writer.write(create_synthetic_frame(frame_index))
    writer.release()
    print(f"Đã tạo video mẫu: {video_output}")


def create_synthetic_frame(frame_index: int) -> np.ndarray:
    image = np.full((480, 640, 3), (185, 200, 210), dtype=np.uint8)
    cv2.rectangle(image, (0, 260), (640, 480), (45, 45, 45), -1)
    cv2.line(image, (320, 270), (320, 470), (255, 255, 255), 4)
    offset = min(160, frame_index * 4)
    cv2.rectangle(image, (210 + offset, 300), (300 + offset, 385), (255, 60, 20), -1)
    cv2.circle(image, (470, 150), 24, (0, 0, 255), -1)
    return image


if __name__ == "__main__":
    main()
