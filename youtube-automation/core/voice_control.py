"""JARVIS V2 voice activation state machine.

This module deliberately separates voice/listening state from the rest of JARVIS.
The backend can remain alive while the UI/listener is deactivated.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ListenerState(str, Enum):
    LISTENING = "listening"
    INACTIVE = "inactive"


@dataclass
class VoiceControl:
    state: ListenerState = ListenerState.LISTENING
    locked: bool = False

    WAKE_PHRASE = "i am vikas"
    ACTIVATE_PHRASES = ("activate system", "continue listening")
    DEACTIVATE_PHRASES = ("deactivate system",)
    LOCK_PHRASES = ("lock",)
    UNLOCK_PHRASES = ("unlock",)

    def normalize(self, text: str) -> str:
        return " ".join(text.lower().strip().split())

    @property
    def listening(self) -> bool:
        return self.state is ListenerState.LISTENING

    def handle(self, text: str) -> ListenerState:
        """Apply one recognized voice command and return the resulting state."""
        command = self.normalize(text)

        if command in self.LOCK_PHRASES:
            self.locked = True
            return self.state

        if command in self.UNLOCK_PHRASES:
            self.locked = False
            return self.state

        # Lock only blocks ordinary activation/deactivation commands. The wake
        # phrase remains the explicit toggle so the UI can be brought back.
        if command == self.WAKE_PHRASE:
            self.state = (
                ListenerState.INACTIVE
                if self.state is ListenerState.LISTENING
                else ListenerState.LISTENING
            )
            return self.state

        if self.locked:
            return self.state

        if command in self.DEACTIVATE_PHRASES:
            self.state = ListenerState.INACTIVE
        elif command in self.ACTIVATE_PHRASES:
            self.state = ListenerState.LISTENING

        return self.state


if __name__ == "__main__":
    import sys

    controller = VoiceControl()
    for phrase in sys.argv[1:]:
        print(f"{phrase!r} -> {controller.handle(phrase).value}")
