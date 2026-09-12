"""UI-independent controller contract for the JARVIS V2 4D VRM avatar.

The controller intentionally contains no renderer/DOM dependency. The locked
 eDEX-UI shell can consume its snapshots through a desktop adapter while the
 core runtime remains independent from the visual implementation.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class VRMState:
    """Render-neutral state that a VRM UI adapter can consume."""

    visible: bool = True
    framing: str = "head_to_waist"
    animation: str = "idle"
    emotion: str = "neutral"
    speaking: bool = False
    listening: bool = False
    lip_sync: bool = True
    mouth_open: float = 0.0
    voice_level: float = 0.0
    locked: bool = False


class VRMController:
    """Translate JARVIS runtime/voice events into deterministic VRM state."""

    def __init__(self, on_change: Callable[[dict[str, Any]], None] | None = None) -> None:
        self._state = VRMState()
        self._on_change = on_change

    def snapshot(self) -> dict[str, Any]:
        """Return JSON-safe state for a UI/renderer adapter."""
        return asdict(self._state)

    def _emit(self) -> None:
        if self._on_change:
            self._on_change(self.snapshot())

    def set_runtime_state(self, state: str, *, locked: bool = False) -> None:
        """Map the canonical runtime state to avatar animation."""
        mapping = {
            "listening": ("listen", "attentive", True),
            "inactive": ("idle", "neutral", False),
            "locked": ("idle", "focused", False),
            "thinking": ("think", "focused", False),
            "speaking": ("speak", "confident", False),
            "error": ("alert", "concerned", False),
        }
        animation, emotion, listening = mapping.get(
            state.lower(), ("idle", "neutral", False)
        )
        self._state = VRMState(
            **{**self.snapshot(), "animation": animation, "emotion": emotion,
               "listening": listening, "locked": locked}
        )
        self._emit()

    def set_emotion(self, emotion: str) -> None:
        """Set an explicit avatar emotion without changing runtime state."""
        self._state = VRMState(**{**self.snapshot(), "emotion": emotion.strip().lower() or "neutral"})
        self._emit()

    def set_voice_level(self, level: float) -> None:
        """Update normalized voice amplitude for HUD/lip-sync animation."""
        level = max(0.0, min(1.0, float(level)))
        mouth_open = min(1.0, level * 1.35) if self._state.speaking else 0.0
        self._state = VRMState(**{**self.snapshot(), "voice_level": level, "mouth_open": mouth_open})
        self._emit()

    def set_speaking(self, speaking: bool) -> None:
        """Toggle speech animation and reset mouth pose when speech ends."""
        speaking = bool(speaking)
        animation = "speak" if speaking else ("listen" if self._state.listening else "idle")
        self._state = VRMState(
            **{**self.snapshot(), "speaking": speaking, "animation": animation,
               "mouth_open": self._state.mouth_open if speaking else 0.0}
        )
        self._emit()

    def set_listening(self, listening: bool) -> None:
        """Toggle listening animation while preserving other avatar state."""
        listening = bool(listening)
        animation = "listen" if listening and not self._state.speaking else ("speak" if self._state.speaking else "idle")
        self._state = VRMState(**{**self.snapshot(), "listening": listening, "animation": animation})
        self._emit()
