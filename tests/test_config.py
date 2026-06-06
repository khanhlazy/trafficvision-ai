from app.config import get_settings


def test_default_config_loads() -> None:
    settings = get_settings()
    assert settings.default_conf > 0
    assert settings.output_dir.exists()
    assert settings.logs_dir.exists()
    assert settings.model_fallback_name.endswith(".pt")
    assert "TrafficVision" in settings.api_title
