"""Hardware-free tests for the JARVIS V2 microphone adapter."""
from __future__ import annotations

import sys
import types

try:
    from .speech_listener import ListenerConfig, SpeechListener
    from .voice_control import VoiceControl
except ImportError:
    from speech_listener import ListenerConfig, SpeechListener
    from voice_control import VoiceControl


def check_microphone_chunk_without_hardware() -> None:
    """Exercise WAV capture/transcription using fake sounddevice/numpy modules."""
    recorded = {"calls": 0, "deleted": False}

    class FakeArray:
        ndim = 2

        def __getitem__(self, key):
            return self

        def tobytes(self):
            return b"\x00\x00" * 160

    fake_numpy = types.SimpleNamespace(
        asarray=lambda value: FakeArray(),
        dtype=lambda value: types.SimpleNamespace(itemsize=2),
    )

    class FakeSoundDevice:
        def rec(self, frames, samplerate, channels, dtype):
            recorded["calls"] += 1
            return [[0]] * frames

        def wait(self):
            return None

    listener = SpeechListener(
        controller=VoiceControl(),
        config=ListenerConfig(chunk_seconds=0.001),
    )
    listener.transcribe = lambda path: "Deactivate system"

    old_numpy = sys.modules.get("numpy")
    old_sd = sys.modules.get("sounddevice")
    sys.modules["numpy"] = fake_numpy
    sys.modules["sounddevice"] = FakeSoundDevice()
    try:
        listener.listen_microphone(max_chunks=1)
    finally:
        if old_numpy is None:
            sys.modules.pop("numpy", None)
        else:
            sys.modules["numpy"] = old_numpy
        if old_sd is None:
            sys.modules.pop("sounddevice", None)
        else:
            sys.modules["sounddevice"] = old_sd

    assert recorded["calls"] == 1
    assert listener.controller.listening is False


if __name__ == "__main__":
    check_microphone_chunk_without_hardware()
    print("speech_listener: OK")
