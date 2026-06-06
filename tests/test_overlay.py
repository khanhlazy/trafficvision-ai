import numpy as np

from app.overlay import blend_segmentation_mask, create_video_writer, draw_boxes, draw_warnings


def test_draw_boxes_returns_same_shape() -> None:
    image = np.zeros((120, 160, 3), dtype=np.uint8)
    predictions = [
        {
            "class_name": "car",
            "class_id": 2,
            "confidence": 0.8,
            "xyxy": [20, 30, 80, 90],
            "area": 3600,
            "center_x": 50,
            "center_y": 60,
        }
    ]
    output = draw_boxes(image, predictions)
    assert output.shape == image.shape


def test_blend_mask_returns_same_shape() -> None:
    image = np.zeros((120, 160, 3), dtype=np.uint8)
    mask = np.zeros((120, 160), dtype=np.uint8)
    mask[60:, 40:120] = 255
    output = blend_segmentation_mask(image, mask)
    assert output.shape == image.shape


def test_draw_warnings_returns_same_shape() -> None:
    image = np.zeros((120, 160, 3), dtype=np.uint8)
    output = draw_warnings(image, ["Thông tin: phát hiện biển báo hoặc đèn giao thông"])
    assert output.shape == image.shape


def test_create_video_writer(tmp_path) -> None:
    writer = create_video_writer(tmp_path / "sample.mp4", 5.0, (160, 120))
    assert writer.isOpened()
    writer.release()
