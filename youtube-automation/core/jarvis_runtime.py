"""JARVIS V2 runtime coordinator."""
from __future__ import annotations

from dataclasses import dataclass
from threading import Lock, Thread
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
    running: bool
    listening: bool
    locked: bool
    state: str
    microphone_running: bool


class JarvisRuntime:
    def __init__(self, controller: Optional[VoiceControl] = None,
                 on_ui_state: Optional[Callable[[bool], None]] = None,
                 microphone: Optional[MicrophoneListener] = None):
        self.controller = controller or VoiceControl()
        self.on_ui_state = on_ui_state
        self.listener = SpeechListener(controller=self.controller, on_state_change=self._state_changed)
        self.microphone = microphone or MicrophoneListener(self.listener)
        self._microphone_thread: Optional[Thread] = None
        self._microphone_lock = Lock()
        self.running = False

    def _state_changed(self, state: str) -> None:
        listening = state == ListenerState.LISTENING.value
        if not listening:
            self.stop_microphone()
        elif self.running:
            self.start_microphone()
        if self.on_ui_state:
            self.on_ui_state(listening)

    def start_microphone(self) -> None:
        with self._microphone_lock:
            if self.microphone.running or (self._microphone_thread and self._microphone_thread.is_alive()):
                return
            self.microphone.running = True
            self._microphone_thread = Thread(target=self.microphone.run, name="jarvis-microphone", daemon=True)
            self._microphone_thread.start()

    def stop_microphone(self) -> None:
        with self._microphone_lock:
            self.microphone.stop()
            self._microphone_thread = None

    def start(self, microphone: bool = False) -> RuntimeStatus:
        self.running = True
        if self.on_ui_state:
            self.on_ui_state(self.controller.listening)
        if microphone and self.controller.listening:
            self.start_microphone()
        return self.status()

    def stop(self) -> RuntimeStatus:
        self.running = False
        self.stop_microphone()
        return self.status()

    def handle_text(self, text: str) -> RuntimeStatus:
        self.listener.process_text(text)
        return self.status()

    def status(self) -> RuntimeStatus:
        return RuntimeStatus(self.running, self.controller.listening, self.controller.locked,
                             self.controller.state.value, self.microphone.running)


if __name__ == "__main__":
    runtime = JarvisRuntime()
    runtime.start()
    for phrase in ("deactivate system", "i am vikas", "lock", "deactivate system", "i am vikas"):
        print(phrase, "->", runtime.handle_text(phrase))
