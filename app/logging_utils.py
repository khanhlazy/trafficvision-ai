"""JSON and CSV logging helpers for inference, warnings, benchmarks, and tests."""

from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np

from app.config import Settings, get_settings


def make_timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")


def sanitize_for_json(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return f"<ndarray shape={value.shape} dtype={value.dtype}>"
    if isinstance(value, Path):
        return str(value)
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if isinstance(value, dict):
        return {key: sanitize_for_json(item) for key, item in value.items() if key not in {"annotated_image", "mask"}}
    if isinstance(value, list):
        return [sanitize_for_json(item) for item in value]
    if isinstance(value, tuple):
        return [sanitize_for_json(item) for item in value]
    return value


def save_run_log(result: dict[str, Any], settings: Settings | None = None, prefix: str = "inference") -> str:
    active_settings = settings or get_settings()
    active_settings.logs_dir.mkdir(parents=True, exist_ok=True)
    timestamp = result.get("timestamp") or make_timestamp()
    path = active_settings.logs_dir / f"{prefix}_{timestamp}.json"
    with path.open("w", encoding="utf-8") as file:
        json.dump(sanitize_for_json(result), file, ensure_ascii=False, indent=2)
    return str(path)


def append_csv_log(row: dict[str, Any], filename: str, settings: Settings | None = None) -> str:
    active_settings = settings or get_settings()
    active_settings.logs_dir.mkdir(parents=True, exist_ok=True)
    path = active_settings.logs_dir / filename
    exists = path.exists()
    with path.open("a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(row.keys()))
        if not exists:
            writer.writeheader()
        writer.writerow(row)
    return str(path)


def save_metrics_log(metrics: dict[str, Any], settings: Settings | None = None, prefix: str = "metrics") -> str:
    active_settings = settings or get_settings()
    payload = {
        "timestamp": metrics.get("timestamp") or make_timestamp(),
        "metrics": metrics,
    }
    return save_run_log(payload, settings=active_settings, prefix=prefix)


def save_ai_agent_log_template(settings: Settings | None = None, filename: str | None = None) -> str:
    active_settings = settings or get_settings()
    active_settings.logs_dir.mkdir(parents=True, exist_ok=True)
    target_name = filename or f"ai_agent_log_template_{make_timestamp()}.md"
    path = active_settings.logs_dir / target_name
    content = """# Mẫu AI Agent Log

| Trường | Nội dung |
|---|---|
| Date |  |
| Topic |  |
| Prompt |  |
| AI response summary |  |
| Decision |  |
| Reason |  |
| Follow-up |  |
"""
    path.write_text(content, encoding="utf-8")
    return str(path)


def save_warning_log(warnings: list[str], metadata: dict[str, Any] | None = None, settings: Settings | None = None) -> str:
    payload = {
        "timestamp": make_timestamp(),
        "warnings": warnings,
        "metadata": metadata or {},
    }
    return save_run_log(payload, settings=settings, prefix="warnings")
