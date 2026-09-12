"""Desktop-facing adapter contract for the locked eDEX JARVIS V2 shell.

This module deliberately does not render HTML/WebGL. It converts the neutral
JARVIS UI snapshot into a stable payload for the eventual eDEX renderer and
keeps the central module fixed to the head-to-waist VRM avatar.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class VRMDisplayConfig:
    module: str = "vrm"
    framing: str = "head_to_waist"
    renderer: str = "webgl-vrm"
    transparent_stage: bool = True
    lip_sync: bool = True
    facial_expression: bool = True
    animation: bool = True


class EDEXVRMAdapter:
    """Build a renderer-neutral payload without changing the eDEX shell."""

    def __init__(self, model_url: str = "assets/vrm/jarvis.vrm") -> None:
        self.config = VRMDisplayConfig()
        self.model_url = model_url

    def mount_payload(self, ui_snapshot: dict[str, Any]) -> dict[str, Any]:
        """Return the exact payload consumed by the desktop renderer."""
        vrm = dict(ui_snapshot.get("vrm") or {})
        vrm.update({
            "visible": True,
            "framing": "head_to_waist",
            "model_url": self.model_url,
            "renderer": self.config.renderer,
            "lip_sync": self.config.lip_sync,
            "facial_expression": self.config.facial_expression,
            "animation": self.config.animation,
        })
        return {
            "shell": "edex",
            "central_module": "vrm",
            "central_framing": "head_to_waist",
            "loading_visible": bool(ui_snapshot.get("loading_visible", False)),
            "transition": ui_snapshot.get("transition", "idle"),
            "voice_status": ui_snapshot.get("voice_status", "inactive"),
            "locked": bool(ui_snapshot.get("locked", False)),
            "vrm": vrm,
            "display_config": asdict(self.config),
        }

    def model_manifest(self) -> dict[str, str]:
        """Describe the runtime asset contract for a future packaged VRM model."""
        return {
            "model_url": self.model_url,
            "format": "VRM",
            "framing": "head_to_waist",
            "placement": "center_terminal_region",
        }
