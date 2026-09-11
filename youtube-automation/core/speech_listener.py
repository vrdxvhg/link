"""Optional speech adapter for JARVIS V2 voice commands."""

from __future__ import annotations

from dataclasses import dataclass
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


class SpeechListener:
    """Transcribe audio locally and route recognized text to VoiceControl."""

    def __init__(self, controller: Optional[VoiceControl] = None,
                 config: Optional[ListenerConfig] = None,
                 on_state_change: Optional[Callable[[str], None]] = None):
        self.controller = controller or VoiceControl()
        self.config = config or ListenerConfig()
        self.on_state_change = on_state_change
        self._model = None

    def process_text(self, text: str) -> str:
        previous = self.controller.listening
        state = self.controller.handle(text)
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
