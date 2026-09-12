"""UI-facing JARVIS runtime facade for the locked eDEX-UI shell.

This keeps the canonical runtime untouched while giving the desktop UI one
stable entry point for runtime state, voice events, and central 4D VRM state.
"""
from __future__ import annotations

from typing import Any, Callable

try:
    from .runtime import JarvisRuntime
    from .ui_state_bridge import EDEXUIStateBridge
except ImportError:
    from runtime import JarvisRuntime
    from ui_state_bridge import EDEXUIStateBridge


class JARVISUIRuntime:
    """Compose JARVIS core runtime with the eDEX/VRM presentation bridge."""

    def __init__(
        self,
        *,
        on_state: Callable[[dict[str, Any]], None] | None = None,
        on_transcript: Callable[[str], None] | None = None,
    ) -> None:
        self.ui = EDEXUIStateBridge()
        self._on_state = on_state
        self.runtime = JarvisRuntime(
            on_ui_state=self._runtime_state_changed,
            on_transcript=on_transcript,
        )
        self.ui.apply_runtime(self.runtime.status()["state"], locked=self.runtime.status()["locked"])

    def _runtime_state_changed(self, state: str) -> None:
        payload = self.ui.apply_runtime(state, locked=self.runtime.controller.locked)
        if self._on_state:
            self._on_state(payload)

    def command(self, text: str) -> str:
        """Run one JARVIS command and return the resulting runtime state."""
        return self.runtime.command(text)

    def snapshot(self) -> dict[str, Any]:
        """Return the renderer payload for the whole desktop UI."""
        return self.ui.snapshot()

    def set_loading(self, visible: bool, *, transition: str = "fade") -> dict[str, Any]:
        return self.ui.set_loading(visible, transition=transition)

    def status(self) -> dict[str, Any]:
        payload = self.snapshot()
        payload["runtime"] = self.runtime.status()
        return payload


if __name__ == "__main__":
    app = JARVISUIRuntime()
    print(app.status())
