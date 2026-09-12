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


def test_ui_command_route():
    client = bridge_app.app.test_client()
    response = client.post("/api/v1/ui/command", json={"command": "Deactivate system"})
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["state"] == "inactive"
    assert payload["ui"]["voice_status"] == "inactive"
