"""Smoke tests for FastAPI prediction endpoints."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app

VALID_FEATURES = {
    "temperature": 73.5,
    "pressure": 5.2,
    "vibration": 2.1,
    "speed": 118.0,
    "humidity": 48.0,
}


@pytest.fixture(scope="module")
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


def test_health(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["model_loaded"] == "True"


def test_model_info(client: TestClient):
    response = client.get("/model-info")
    assert response.status_code == 200
    payload = response.json()
    assert "temperature" in payload["features"]
    assert payload["model_type"] == "RandomForestClassifier"
    assert "accuracy" in payload["metrics"]


def test_predict_success(client: TestClient):
    response = client.post("/predict", json={"features": VALID_FEATURES})
    assert response.status_code == 200
    payload = response.json()
    assert payload["prediction"] in {"normal", "defect"}
    assert payload["risk_level"] in {"low", "medium", "high"}
    assert payload["recommendation"]


def test_predict_missing_features(client: TestClient):
    response = client.post(
        "/predict",
        json={"features": {"temperature": 73.5}},
    )
    assert response.status_code == 422
    detail = response.json()["detail"]
    assert detail["error"] == "missing_features"
