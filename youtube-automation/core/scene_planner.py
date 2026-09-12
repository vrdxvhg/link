"""Adaptive cinematic scene planning for song-driven videos."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class Scene:
    index: int
    start_seconds: float
    end_seconds: float
    visual_style: str
    transition: str
    beat_sync: bool = True


def build_beat_timeline(duration_seconds: float, bpm: float = 120.0) -> list[float]:
    """Return beat timestamps from zero through the final beat inside the audio."""
    if duration_seconds <= 0:
        raise ValueError("duration_seconds must be greater than zero")
    if bpm <= 0:
        raise ValueError("bpm must be greater than zero")

    beat = 60.0 / bpm
    count = int((duration_seconds - 1e-9) / beat) + 1
    return [round(index * beat, 6) for index in range(count)]


def build_scene_plan(
    duration_seconds: float, bpm: float = 120.0, mood: str = "cinematic"
) -> dict[str, Any]:
    """Create a deterministic first-pass storyboard aligned to eight-beat blocks."""
    if duration_seconds <= 0:
        raise ValueError("duration_seconds must be greater than zero")
    if bpm <= 0:
        raise ValueError("bpm must be greater than zero")

    beat = 60.0 / bpm
    block = beat * 8.0
    count = max(1, int((duration_seconds + block - 1e-9) // block))
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
        start = min(duration_seconds, index * block)
        end = min(duration_seconds, start + block)
        if end <= start:
            continue
        scenes.append(Scene(index + 1, start, end, style, "beat_cut"))

    # Keep the final scene boundary exactly equal to the media duration.
    if scenes:
        scenes[-1].end_seconds = duration_seconds

    return {
        "version": "1.1",
        "duration_seconds": duration_seconds,
        "bpm": bpm,
        "mood": mood,
        "beat_seconds": beat,
        "beat_timeline": build_beat_timeline(duration_seconds, bpm),
        "scenes": [asdict(scene) for scene in scenes],
    }
