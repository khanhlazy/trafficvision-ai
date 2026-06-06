import numpy as np

from app.config import Settings
from app.inference import TrafficAIPipeline


def test_pipeline_runs_on_blank_image_without_crashing(tmp_path) -> None:
    settings = Settings(
        det_model_path=tmp_path / "missing_detector.pt",
        seg_model_path=tmp_path / "missing_segmenter.pth",
        output_dir=tmp_path / "outputs",
        default_conf=0.35,
        enable_segmentation=True,
        enable_tracking=True,
        save_logs=True,
        allow_model_download=False,
    )
    settings.ensure_directories()
    pipeline = TrafficAIPipeline(settings=settings)
    image = np.zeros((240, 320, 3), dtype=np.uint8)
    result = pipeline.process_image(image, save_output=True)
    assert result["status"] == "ok"
    assert result["annotated_image"].shape == image.shape
    assert result["segmentation_mode"] == "Chế độ phân vùng demo"
    assert result["segmentation_info"]["is_fallback"] is True
    assert result["log_path"].endswith(".json")
