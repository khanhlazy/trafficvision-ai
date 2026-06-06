import json

from app.config import Settings
from app.logging_utils import save_ai_agent_log_template, save_metrics_log, save_run_log


def test_pipeline_can_save_json_logs(tmp_path) -> None:
    settings = Settings(output_dir=tmp_path)
    settings.ensure_directories()
    payload = {
        "timestamp": "20260606_000000_000000",
        "predictions": [],
        "warnings": ["Trạng thái an toàn: chưa phát hiện nguy cơ rõ ràng"],
        "fps": 10.0,
    }
    path = save_run_log(payload, settings=settings)
    loaded = json.loads(open(path, encoding="utf-8").read())
    assert loaded["warnings"]
    assert path.endswith(".json")


def test_metrics_and_ai_agent_log_helpers(tmp_path) -> None:
    settings = Settings(output_dir=tmp_path)
    settings.ensure_directories()
    metrics_path = save_metrics_log({"fps": 12.5}, settings=settings)
    agent_log_path = save_ai_agent_log_template(settings=settings)
    assert metrics_path.endswith(".json")
    assert agent_log_path.endswith(".md")
