"""Live microphone adapter for JARVIS V2.

Optional runtime layer: sounddevice captures short WAV chunks and
SpeechListener transcribes them locally with faster-whisper.
"""

from __future__ import annotations

import tempfile
import wave
from pathlib import Path
from typing import Optional

from speech_listener import SpeechListener


class MicrophoneListener:
    def __init__(self, listener: Optional[SpeechListener] = None):
        self.listener = listener or SpeechListener()
        self.running = False

    def listen_once(self) -> str:
        try:
            import numpy as np
            import sounddevice as sd
        except ImportError as exc:
            raise RuntimeError(
                "Optional microphone dependencies missing: install "
                "sounddevice and numpy."
            ) from exc

        frames = int(self.listener.config.sample_rate * self.listener.config.chunk_seconds)
        audio = sd.rec(
            frames,
            samplerate=self.listener.config.sample_rate,
            channels=1,
            dtype="int16",
        )
        sd.wait()

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            wav_path = Path(tmp.name)
        try:
            with wave.open(str(wav_path), "wb") as wav:
                wav.setnchannels(1)
                wav.setsampwidth(np.dtype(np.int16).itemsize)
                wav.setframerate(self.listener.config.sample_rate)
                wav.writeframes(audio.tobytes())
            return self.listener.process_audio_file(str(wav_path))
        finally:
            wav_path.unlink(missing_ok=True)

    def run(self) -> None:
        self.running = True
        try:
            while self.running and self.listener.controller.listening:
                self.listen_once()
        finally:
            self.running = False

    def stop(self) -> None:
        self.running = False
