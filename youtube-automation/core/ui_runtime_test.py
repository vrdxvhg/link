"""Dependency-light tests for the eDEX/VRM UI runtime facade."""
from __future__ import annotations

try:
    from .ui_runtime import JARVISUIRuntime
except ImportError:
    from ui_runtime import JARVISUIRuntime


def check_initial_snapshot() -> None:
    app = JARVISUIRuntime()
    snapshot = app.snapshot()
    assert snapshot["shell"] == "edex"
    assert snapshot["central_module"] == "vrm"
    assert snapshot["central_framing"] == "head_to_waist"
    assert snapshot["vrm"]["framing"] == "head_to_waist"
    assert snapshot["vrm"]["lip_sync"] is True


def check_runtime_state_updates() -> None:
    app = JARVISUIRuntime()
    assert app.command("Deactivate system") == "inactive"
    snapshot = app.snapshot()
    assert snapshot["voice_status"] == "inactive"
    assert snapshot["vrm"]["animation"] == "idle"
    assert snapshot["vrm"]["listening"] is False

    assert app.command("I am Vikas") == "listening"
    snapshot = app.snapshot()
    assert snapshot["voice_status"] == "listening"
    assert snapshot["vrm"]["animation"] == "listen"
    assert snapshot["vrm"]["listening"] is True


def check_loading_contract() -> None:
    app = JARVISUIRuntime()
    snapshot = app.set_loading(True, transition="fade_in")
    assert snapshot["loading_visible"] is True
    assert snapshot["transition"] == "fade_in"
    assert snapshot["central_module"] == "vrm"


if __name__ == "__main__":
    check_initial_snapshot()
    check_runtime_state_updates()
    check_loading_contract()
    print("ui_runtime: OK")
