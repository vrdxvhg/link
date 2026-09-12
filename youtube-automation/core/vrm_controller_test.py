"""Dependency-light tests for the render-neutral JARVIS VRM controller."""
from __future__ import annotations

try:
    from .vrm_controller import VRMController
except ImportError:
    from vrm_controller import VRMController


def check_runtime_mapping() -> None:
    events = []
    controller = VRMController(events.append)

    controller.set_runtime_state("listening")
    state = controller.snapshot()
    assert state["framing"] == "head_to_waist"
    assert state["animation"] == "listen"
    assert state["listening"] is True
    assert state["lip_sync"] is True
    assert events[-1] == state

    controller.set_runtime_state("speaking")
    controller.set_speaking(True)
    controller.set_voice_level(0.8)
    state = controller.snapshot()
    assert state["animation"] == "speak"
    assert state["speaking"] is True
    assert state["mouth_open"] > 0.0
    assert state["voice_level"] == 0.8


def check_normalization_and_lock() -> None:
    controller = VRMController()
    controller.set_runtime_state("LISTENING", locked=True)
    controller.set_voice_level(2.0)
    assert controller.snapshot()["locked"] is True
    assert controller.snapshot()["voice_level"] == 1.0

    controller.set_speaking(False)
    assert controller.snapshot()["mouth_open"] == 0.0
    controller.set_emotion("  Happy  ")
    assert controller.snapshot()["emotion"] == "happy"


if __name__ == "__main__":
    check_runtime_mapping()
    check_normalization_and_lock()
    print("vrm_controller: OK")
