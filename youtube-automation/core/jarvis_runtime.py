"""JARVIS V2 runtime coordinator."""

from __future__ import annotations

from dataclasses import dataclass
from threading import Thread
from typing import Callable, Optional

try:
    from .voice_control import ListenerState, VoiceControl
    from .speech_listener import SpeechListener
    from .microphone_listener import MicrophoneListener
except ImportError:
    from voice_control import ListenerState, VoiceControl
    from speech_listener import SpeechListener
    from microphone_listener import MicrophoneListener


@dataclass
class RuntimeStatus:
    listening: bool
    locked: bool
    state: str
    microphone_running: bool


class JarvisRuntime:
    def __init__(self, controller: Optional[VoiceControl] = None,
                 on_ui_state: Optional[Callable[[bool], None]] = None):
        self.controller = controller or VoiceControl()
        self.on_ui_state = on_ui_state
        self.listener = SpeechListener(
            controller=self.controller,
            on_state_change=self._state_changed,
        )
        self.microphone = MicrophoneListener(self.listener)
        self._microphone_thread: Optional[Thread] = None
        self.running = False

    def _state_changed(self, state: str) -> None:
        listening = state == ListenerState.LISTENING.value
        if not listening:
            self.microphone.stop()
        elif self.running:
            self._start_microphone()
        if self.on_ui_state:
            self.on_ui_state(listening)

    def _start_microphone(self) -> None:
        if self.microphone.running:
            return
        self.microphone.running = True
        self._microphone_thread = Thread(
            target=self.microphone.run,
            name="jarvis-microphone",
            daemon=True,
        )
        self._microphone_thread.start()

    def start(self, microphone: bool = True) -> RuntimeStatus:
        self.running = True
        self._state_changed(self.controller.state.value)
        if microphone and self.controller.listening:
            self._start_microphone()
        return self.status()

    def stop(self) -> RuntimeStatus:
        self.running = False
        self.microphone.stop()
        return self.status()

    def handle_text(self, text: str) -> RuntimeStatus:
        self.listener.process_text(text)
        return self.status()

    def status(self) -> RuntimeStatus:
        return RuntimeStatus(
            listening=self.controller.listening,
            locked=self.controller.locked,
            state=self.controller.state.value,
            microphone_running=self.microphone.running,
        )


if __name__ == "__main__":
    runtime = JarvisRuntime()
    runtime.start(microphone=False)
    print(runtime.status())
    for phrase in ("deactivate system", "i am vikas", "lock", "deactivate system", "i am vikas"):
        print(phrase, "->", runtime.handle_text(phrase))
