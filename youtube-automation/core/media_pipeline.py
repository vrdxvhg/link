"""JARVIS V2 media pipeline orchestration helpers.

This module is intentionally thin: planning stays in the media-plan layer,
while rendering remains owned by the FFmpeg timeline renderer. The adapter
keeps those concerns connected without coupling either layer to a UI.
"""
from __future__ import annotations

from pathlib import Path

try:
    from .shorts_media_adapters import ShortsMediaPlan
    from .timeline_renderer import render_timeline
except ImportError:
    from shorts_media_adapters import ShortsMediaPlan
    from timeline_renderer import render_timeline


def render_media_plan(
    plan: ShortsMediaPlan,
    output_path: str,
    *,
    width: int = 1920,
    height: int = 1080,
    fps: int = 30,
) -> str:
    """Render a validated JARVIS media plan through the canonical renderer."""
    plan.validate()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    return render_timeline(
        plan.segments,
        str(output),
        width=width,
        height=height,
        fps=fps,
    )
