"""JARVIS V2 runtime coordinator.

Keeps the backend alive while the voice/UI interaction layer can be activated
or deactivated by VoiceControl. The runtime is intentionally independent of a
specific GUI or microphone implementation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

try:
    from .voice_control import ListenerState, VoiceControl
    from .speech_listener import SpeechListener
except ImportError:
    from voice_control import ListenerState, VoiceControl
    from speech_listener import SpeechListener


@dataclass
class RuntimeStatus:
    listening: bool
    locked: bool
    state: str


class JarvisRuntime:
    def __init__(self, controller: Optional[VoiceControl] = None,
                 on_ui_state: Optional[Callable[[bool], None]] = None):
        self.controller = controller or VoiceControl()
        self.on_ui_state = on_ui_state
        self.listener = SpeechListener(
            controller=self.controller,
            on_state_change=self._state_changed,
        )
        self.running = False

    def _state_changed(self, state: str) -> None:
        if self.on_ui_state:
            self.on_ui_state(state == ListenerState.LISTENING.value)

    def start(self) -> RuntimeStatus:
        self.running = True
        self._state_changed(self.controller.state.value)
        return self.status()

    def stop(self) -> RuntimeStatus:
        self.running = False
        return self.status()

    def handle_text(self, text: str) -> RuntimeStatus:
        self.listener.process_text(text)
        return self.status()

    def status(self) -> RuntimeStatus:
        return RuntimeStatus(
            listening=self.controller.listening,
            locked=self.controller.locked,
            state=self.controller.state.value,
        )


if __name__ == "__main__":
    runtime = JarvisRuntime()
    runtime.start()
    print(runtime.status())
    for phrase in ("deactivate system", "i am vikas", "lock", "deactivate system", "i am vikas"):
        print(phrase, "->", runtime.handle_text(phrase))
