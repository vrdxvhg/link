from security_center import SecurityCenter


def test_status():
    result = SecurityCenter().status()
    assert result["status"] == "ready"
    assert result["scope"] == "local/authorized"


def test_blocked_command():
    code, out, err = SecurityCenter().run_local_command("shutdown /s")
    assert code == 3
    assert "blocked" in err.lower()


def test_empty_command():
    code, out, err = SecurityCenter().run_local_command("")
    assert code == 2


def test_voice_status_route():
    handled, output = SecurityCenter().route_voice_command("security status")
    assert handled is True
    assert "Security Center" in output
