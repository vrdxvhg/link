"""Optional microphone adapter for JARVIS V2 voice commands.

The state machine remains usable without this dependency. Install the optional
speech stack only on machines where microphone control is required.

Recommended local backend: faster-whisper + sounddevice. Whisper supports
multilingual speech recognition and local inference; the adapter intentionally
keeps recognition separate from command/state handling.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

from voice_control import VoiceControl


@dataclass
class ListenerConfig:
    model: str = "base"
    language: Optional[str] = None
    sample_rate: int = 16000
    chunk_seconds: float = 4.0


class SpeechListener:
    """Bridge recognized text into VoiceControl.

    This class does not start a microphone by itself. A concrete recorder can
    provide audio chunks to ``process_audio_file`` or ``process_text``. This
    keeps hardware and ASR dependencies out of the core state machine.
    """

    def __init__(self, controller: Optional[VoiceControl] = None,
                 config: Optional[ListenerConfig] = None,
                 on_state_change: Optional[Callable[[str], None]] = None):
        self.controller = controller or VoiceControl()
        self.config = config or ListenerConfig()
        self.on_state_change = on_state_change

    def process_text(self, text: str) -> str:
        previous = self.controller.listening
        state = self.controller.handle(text)
        if self.on_state_change and previous != self.controller.listening:
            self.on_state_change(state.value)
        return state.value

    def process_audio_file(self, audio_path: str) -> str:
        """Transcribe one short clip with faster-whisper when installed."""
        try:
            from faster_whisper import WhisperModel
        except ImportError as exc:
            raise RuntimeError(
                "Optional dependency missing: install faster-whisper to use "
                "microphone/audio recognition."
            ) from exc

        model = WhisperModel(self.config.model, device="auto", compute_type="auto")
        segments, _ = model.transcribe(
            audio_path,
            language=self.config.language,
            vad_filter=True,
        )
        text = " ".join(segment.text.strip() for segment in segments).strip()
        return self.process_text(text)
