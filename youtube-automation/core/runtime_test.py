from runtime import JarvisRuntime


def check():
    events = []
    runtime = JarvisRuntime(on_ui_state=events.append)

    assert runtime.status() == {
        "backend": "running",
        "listening": True,
        "locked": False,
        "state": "listening",
    }

    assert runtime.command("Deactivate system") == "inactive"
    assert runtime.status()["backend"] == "running"
    assert runtime.status()["listening"] is False
    assert events[-1] == "inactive"

    assert runtime.command("I am Vikas") == "listening"
    assert events[-1] == "listening"

    runtime.command("lock")
    assert runtime.status()["locked"] is True
    runtime.command("deactivate system")
    assert runtime.listening is True

    runtime.command("I am Vikas")
    assert runtime.listening is False


if __name__ == "__main__":
    check()
    print("runtime: OK")
