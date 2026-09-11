from voice_vad import is_speech, rms_level


def test_silence_is_not_speech():
    assert rms_level([0, 0, 0, 0]) == 0.0
    assert is_speech([0] * 1000) is False


def test_voice_level_passes_gate():
    assert is_speech([1000, -1000] * 1000) is True


if __name__ == "__main__":
    test_silence_is_not_speech()
    test_voice_level_passes_gate()
    print("voice VAD tests: PASS")
