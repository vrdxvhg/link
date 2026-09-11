"""JARVIS V2 runtime coordinator for voice activation and UI state.

The runtime keeps the backend alive while the interaction layer is inactive.
A UI can subscribe to state changes without knowing anything about speech recognition.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional

from .voice_control import ListenerState, VoiceControl
from .speech_listener import ListenerConfig, SpeechListener


@dataclass
class JarvisRuntime:
    controller: VoiceControl = field(default_factory=VoiceControl)
    on_ui_state: Optional[Callable[[str], None]] = None

    def __post_init__(self) -> None:
        self.listener = SpeechListener(
            controller=self.controller,
            config=ListenerConfig(),
            on_state_change=self._state_changed,
        )

    @property
    def listening(self) -> bool:
        return self.controller.state is ListenerState.LISTENING

    def _state_changed(self, state: str) -> None:
        if self.on_ui_state:
            self.on_ui_state(state)

    def command(self, text: str) -> str:
        """Route recognized text into the voice-control state machine."""
        return self.listener.process_text(text)

    def audio_file(self, path: str) -> str:
        """Route a recorded speech clip through the ASR adapter."""
        return self.listener.process_audio_file(path)

    def status(self) -> dict:
        return {
            "backend": "running",
            "listening": self.listening,
            "locked": self.controller.locked,
            "state": self.controller.state.value,
        }


if __name__ == "__main__":
    runtime = JarvisRuntime(on_ui_state=lambda state: print(f"UI: {state}"))
    print(runtime.status())
    import sys
    for command in sys.argv[1:]:
        print(command, "->", runtime.command(command), runtime.status())
