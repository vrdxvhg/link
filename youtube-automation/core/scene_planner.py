"""Adaptive cinematic scene planning for song-driven videos."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class Scene:
    index: int
    start_seconds: float
    end_seconds: float
    visual_style: str
    transition: str
    beat_sync: bool = True


def build_scene_plan(duration_seconds: float, bpm: float = 120.0, mood: str = "cinematic") -> dict[str, Any]:
    """Create a deterministic first-pass storyboard without rendering anything."""
    beat = 60.0 / max(bpm, 1.0)
    block = beat * 8.0
    count = max(1, int((duration_seconds + block - 0.001) // block))
    scenes: list[Scene] = []
    styles = {
        "romantic": "cinematic_romance",
        "sad": "emotional_cinematic",
        "devotional": "spiritual_cinematic",
        "energetic": "performance_neon",
        "punjabi": "punjabi_cinematic_3d",
        "village": "stylized_rural_3d",
    }
    style = styles.get(mood.lower(), "cinematic_3d")
    for index in range(count):
        start = index * block
        end = min(duration_seconds, start + block)
        scenes.append(Scene(index + 1, start, end, style, "beat_cut"))
    return {"version": "1.0", "duration_seconds": duration_seconds, "bpm": bpm, "mood": mood, "scenes": [asdict(s) for s in scenes]}
