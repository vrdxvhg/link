"""Optional local speech adapter for JARVIS V2 voice commands."""

from __future__ import annotations

from dataclasses import dataclass
import tempfile
import time
import wave
from typing import Callable, Optional

try:
    from .voice_control import VoiceControl
except ImportError:
    from voice_control import VoiceControl


@dataclass
class ListenerConfig:
    model: str = "base"
    language: Optional[str] = None
    sample_rate: int = 16000
    chunk_seconds: float = 4.0
    channels: int = 1
    dtype: str = "int16"


class SpeechListener:
    """Transcribe local audio and route recognized text to VoiceControl.

    Microphone capture is optional and imported lazily so the core runtime can
    still start on machines that do not have the audio stack installed.
    """

    def __init__(self, controller: Optional[VoiceControl] = None,
                 config: Optional[ListenerConfig] = None,
                 on_state_change: Optional[Callable[[str], None]] = None,
                 on_transcript: Optional[Callable[[str], None]] = None):
        self.controller = controller or VoiceControl()
        self.config = config or ListenerConfig()
        self.on_state_change = on_state_change
        self.on_transcript = on_transcript
        self._model = None
        self._stop_requested = False

    def process_text(self, text: str) -> str:
        text = (text or "").strip()
        if not text:
            return self.controller.state.value
        previous = self.controller.listening
        state = self.controller.handle(text)
        if self.on_transcript:
            self.on_transcript(text)
        if self.on_state_change and previous != self.controller.listening:
            self.on_state_change(state.value)
        return state.value

    def _get_model(self):
        if self._model is None:
            try:
                from faster_whisper import WhisperModel
            except ImportError as exc:
                raise RuntimeError(
                    "Optional dependency missing: install faster-whisper."
                ) from exc
            self._model = WhisperModel(
                self.config.model, device="auto", compute_type="auto"
            )
        return self._model

    def transcribe(self, audio_path: str) -> str:
        segments, _ = self._get_model().transcribe(
            audio_path,
            language=self.config.language,
            vad_filter=True,
        )
        return " ".join(segment.text.strip() for segment in segments).strip()

    def process_audio_file(self, audio_path: str) -> str:
        return self.process_text(self.transcribe(audio_path))

    def request_stop(self) -> None:
        """Request the microphone loop to stop after its current chunk."""
        self._stop_requested = True

    def listen_microphone(self, max_chunks: Optional[int] = None) -> None:
        """Capture short microphone chunks and route each through ASR.

        The loop only runs while VoiceControl is listening. It never owns or
        shuts down the JARVIS backend; callers control the runtime lifecycle.
        """
        try:
            import numpy as np
            import sounddevice as sd
        except ImportError as exc:
            raise RuntimeError(
                "Optional microphone dependencies missing: install sounddevice and numpy."
            ) from exc

        self._stop_requested = False
        chunk_index = 0
        frames = max(1, int(self.config.sample_rate * self.config.chunk_seconds))

        while not self._stop_requested and self.controller.listening:
            recording = sd.rec(
                frames,
                samplerate=self.config.sample_rate,
                channels=self.config.channels,
                dtype=self.config.dtype,
            )
            sd.wait()

            if self._stop_requested:
                break

            samples = np.asarray(recording)
            if self.config.channels == 1 and samples.ndim == 2:
                samples = samples[:, 0]

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                wav_path = tmp.name

            try:
                with wave.open(wav_path, "wb") as wav:
                    wav.setnchannels(self.config.channels)
                    wav.setsampwidth(np.dtype(self.config.dtype).itemsize)
                    wav.setframerate(self.config.sample_rate)
                    wav.writeframes(samples.tobytes())
                transcript = self.transcribe(wav_path)
                if transcript:
                    self.process_text(transcript)
            finally:
                try:
                    import os
                    os.unlink(wav_path)
                except OSError:
                    pass

            chunk_index += 1
            if max_chunks is not None and chunk_index >= max_chunks:
                break

            # Give the state machine a chance to turn listening off between chunks.
            time.sleep(0.01)
