"""Dependency-light tests for the JARVIS V2 runtime coordinator."""
from __future__ import annotations

import time

try:
    from .runtime import JarvisRuntime
except ImportError:
    from runtime import JarvisRuntime


def _fake_microphone(runtime: JarvisRuntime, max_chunks=None) -> None:
    while not runtime.listener._stop_requested:
        time.sleep(0.005)


def check_state_machine() -> None:
    events = []
    runtime = JarvisRuntime(on_ui_state=events.append)
    runtime.listener.listen_microphone = lambda max_chunks=None: _fake_microphone(runtime, max_chunks)

    status = runtime.status()
    assert status["backend"] == "running"
    assert status["listening"] is True
    assert status["microphone_running"] is False
    assert status["locked"] is False
    assert status["state"] == "listening"

    assert runtime.command("Deactivate system") == "inactive"
    assert runtime.status()["backend"] == "running"
    assert runtime.status()["listening"] is False
    assert runtime.microphone_running is False
    assert events[-1] == "inactive"

    assert runtime.command("I am Vikas") == "listening"
    assert events[-1] == "listening"
    assert runtime.status()["backend"] == "running"
    assert runtime.microphone_running is True

    runtime.command("lock")
    assert runtime.status()["locked"] is True
    runtime.command("deactivate system")
    assert runtime.listening is True

    runtime.command("I am Vikas")
    assert runtime.listening is False
    assert runtime.microphone_running is False


def check_microphone_lifecycle_without_hardware() -> None:
    """Verify runtime thread lifecycle without opening a real microphone."""
    runtime = JarvisRuntime()
    runtime.listener.listen_microphone = lambda max_chunks=None: _fake_microphone(runtime, max_chunks)

    assert runtime.microphone_running is False
    runtime.start_microphone()
    assert runtime.microphone_running is True

    runtime.stop_microphone()
    assert runtime.microphone_running is False


if __name__ == "__main__":
    check_state_machine()
    check_microphone_lifecycle_without_hardware()
    print("runtime: OK")
