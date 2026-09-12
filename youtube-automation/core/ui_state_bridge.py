"""Runtime-to-eDEX UI state bridge for JARVIS V2.

The bridge keeps the locked eDEX-UI shell independent from JARVIS Core details.
It exposes one JSON-safe snapshot containing runtime state and the central 4D
VRM avatar state. A desktop renderer can consume this snapshot without putting
DOM or renderer dependencies into the core runtime.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

try:
    from .vrm_controller import VRMController
except ImportError:
    from vrm_controller import VRMController


@dataclass(frozen=True)
class EDEXUIState:
    """Render-neutral shell state for the locked eDEX-style desktop UI."""

    shell: str = "edex"
    voice_status: str = "listening"
    locked: bool = False
    central_module: str = "vrm"
    central_framing: str = "head_to_waist"
    loading_visible: bool = False
    transition: str = "idle"
    vrm: dict[str, Any] | None = None


class EDEXUIStateBridge:
    """Combine runtime state and VRM state for the desktop presentation layer."""

    def __init__(self) -> None:
        self.vrm = VRMController()
        self._state = EDEXUIState(vrm=self.vrm.snapshot())

    def apply_runtime(self, state: str, *, locked: bool = False) -> dict[str, Any]:
        """Update shell/VRM state from the canonical runtime state string."""
        normalized = state.strip().lower() or "inactive"
        self.vrm.set_runtime_state(normalized, locked=locked)
        self._state = EDEXUIState(
            shell="edex",
            voice_status=normalized,
            locked=locked,
            central_module="vrm",
            central_framing="head_to_waist",
            loading_visible=False,
            transition="state_change",
            vrm=self.vrm.snapshot(),
        )
        return self.snapshot()

    def set_loading(self, visible: bool, *, transition: str = "fade") -> dict[str, Any]:
        """Preserve eDEX loading/transition semantics without changing the shell."""
        self._state = EDEXUIState(
            **{
                **asdict(self._state),
                "loading_visible": bool(visible),
                "transition": transition,
                "vrm": self.vrm.snapshot(),
            }
        )
        return self.snapshot()

    def snapshot(self) -> dict[str, Any]:
        """Return the complete UI payload for a desktop renderer."""
        return asdict(self._state)
