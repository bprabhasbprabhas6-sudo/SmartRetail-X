import logging

from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "SmartRetail-X API"


def test_health_request_is_logged(caplog):
    with caplog.at_level(logging.INFO, logger="smartretail"):
        response = client.get("/health")

    assert response.status_code == 200

    messages = [record.getMessage() for record in caplog.records]

    assert any(
        "Request started | method=GET | path=/health" in message
        for message in messages
    )

    assert any(
        "Request completed | method=GET | path=/health | status=200"
        in message
        for message in messages
    )