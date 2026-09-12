"""Dependency-light tests for the bridge UI state/command surface."""
from __future__ import annotations

from . import app as bridge_app


def test_ui_state_route():
    client = bridge_app.app.test_client()
    response = client.get("/api/v1/ui/state")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["shell"] == "edex"
    assert payload["central_module"] == "vrm"
    assert payload["central_framing"] == "head_to_waist"
    assert payload["vrm"]["framing"] == "head_to_waist"


def test_ui_command_route():
    client = bridge_app.app.test_client()
    response = client.post("/api/v1/ui/command", json={"command": "Deactivate system"})
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["state"] == "inactive"
    assert payload["ui"]["voice_status"] == "inactive"
    assert payload["ui"]["vrm"]["listening"] is False


def test_ui_command_requires_command():
    client = bridge_app.app.test_client()
    response = client.post("/api/v1/ui/command", json={})
    assert response.status_code == 400
    assert response.get_json()["error"] == "command is required"


def test_ui_preflight_and_cors():
    client = bridge_app.app.test_client()
    response = client.options(
        "/api/v1/ui/command",
        headers={"Origin": "http://127.0.0.1:8000"},
    )
    assert response.status_code == 204
    assert response.headers["Access-Control-Allow-Origin"] == "http://127.0.0.1:8000"
    assert "POST" in response.headers["Access-Control-Allow-Methods"]
