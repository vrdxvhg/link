"""Tests for the JARVIS V2 runtime coordinator."""

from jarvis_runtime import JarvisRuntime


def test_runtime_stays_alive_when_listener_is_inactive():
    runtime = JarvisRuntime()
    runtime.start()
    runtime.handle_text("deactivate system")
    assert runtime.running is True
    assert runtime.status().listening is False


def test_wake_phrase_restores_listener():
    runtime = JarvisRuntime()
    runtime.start()
    runtime.handle_text("deactivate system")
    runtime.handle_text("i am vikas")
    assert runtime.status().listening is True


def test_lock_blocks_normal_deactivation():
    runtime = JarvisRuntime()
    runtime.start()
    runtime.handle_text("lock")
    runtime.handle_text("deactivate system")
    assert runtime.status().listening is True
    assert runtime.status().locked is True


if __name__ == "__main__":
    test_runtime_stays_alive_when_listener_is_inactive()
    test_wake_phrase_restores_listener()
    test_lock_blocks_normal_deactivation()
    print("jarvis runtime tests: PASS")
