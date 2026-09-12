"""JARVIS V2 runtime coordinator for voice activation and UI state.

The runtime keeps the backend alive while the interaction layer is inactive.
A UI can subscribe to state changes without knowing anything about speech recognition.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import threading
from typing import Callable, Optional

try:
    from .voice_control import ListenerState, VoiceControl
    from .speech_listener import ListenerConfig, SpeechListener
except ImportError:  # Allow direct execution from the core directory.
    from voice_control import ListenerState, VoiceControl
    from speech_listener import ListenerConfig, SpeechListener


@dataclass
class JarvisRuntime:
    controller: VoiceControl = field(default_factory=VoiceControl)
    on_ui_state: Optional[Callable[[str], None]] = None
    on_transcript: Optional[Callable[[str], None]] = None

    def __post_init__(self) -> None:
        self.listener = SpeechListener(
            controller=self.controller,
            config=ListenerConfig(),
            on_state_change=self._state_changed,
            on_transcript=self.on_transcript,
        )
        self._mic_thread: Optional[threading.Thread] = None

    @property
    def listening(self) -> bool:
        return self.controller.state is ListenerState.LISTENING

    @property
    def microphone_running(self) -> bool:
        return bool(self._mic_thread and self._mic_thread.is_alive())

    def _state_changed(self, state: str) -> None:
        if self.on_ui_state:
            self.on_ui_state(state)

    def command(self, text: str) -> str:
        """Route recognized text into the voice-control state machine."""
        state = self.listener.process_text(text)
        if self.listening and not self.microphone_running:
            self.start_microphone()
        elif not self.listening:
            self.stop_microphone()
        return state

    def audio_file(self, path: str) -> str:
        """Route a recorded speech clip through the ASR adapter."""
        return self.listener.process_audio_file(path)

    def start_microphone(self) -> None:
        """Start optional microphone capture without blocking backend services."""
        if self.microphone_running or not self.listening:
            return
        self.listener._stop_requested = False
        self._mic_thread = threading.Thread(
            target=self.listener.listen_microphone,
            name="jarvis-microphone",
            daemon=True,
        )
        self._mic_thread.start()

    def stop_microphone(self) -> None:
        """Stop microphone capture without stopping JARVIS backend services."""
        self.listener.request_stop()
        thread = self._mic_thread
        if thread and thread.is_alive() and thread is not threading.current_thread():
            thread.join(timeout=max(1.0, self.listener.config.chunk_seconds + 1.0))
        self._mic_thread = None

    def status(self) -> dict:
        return {
            "backend": "running",
            "listening": self.listening,
            "microphone_running": self.microphone_running,
            "locked": self.controller.locked,
            "state": self.controller.state.value,
        }


if __name__ == "__main__":
    runtime = JarvisRuntime(on_ui_state=lambda state: print(f"UI: {state}"))
    print(runtime.status())
    import sys
    for command in sys.argv[1:]:
        print(command, "->", runtime.command(command), runtime.status())
