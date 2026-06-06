from fastapi.testclient import TestClient

from app.api import app


def test_health_returns_ok() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert "model_info" in payload
    assert "segmentation_info" in payload
