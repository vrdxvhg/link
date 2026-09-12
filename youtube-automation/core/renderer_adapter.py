"""Pluggable visual renderer contract for JARVIS V2.

The core pipeline depends only on this interface so a real 3D renderer can replace
FFmpeg's MVP background renderer without changing job orchestration.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class VisualRenderer(ABC):
    @abstractmethod
    def render(self, audio_path: str, scene_plan: dict[str, Any], output_path: str) -> str:
        """Render the scene plan into an MP4 file."""
        raise NotImplementedError


class FfmpegMvpRenderer(VisualRenderer):
    """Adapter around the existing FFmpeg renderer."""

    def __init__(self, mood: str = "cinematic") -> None:
        self.mood = mood

    def render(self, audio_path: str, scene_plan: dict[str, Any], output_path: str) -> str:
        from .render_engine import render_song_video
        return render_song_video(audio_path, output_path, mood=self.mood)


class RendererRegistry:
    """Named renderer registry used by the pipeline and future UI settings."""

    def __init__(self) -> None:
        self._renderers: dict[str, VisualRenderer] = {}

    def register(self, name: str, renderer: VisualRenderer) -> None:
        key = name.strip().lower()
        if not key:
            raise ValueError("renderer name is required")
        self._renderers[key] = renderer

    def get(self, name: str) -> VisualRenderer:
        key = name.strip().lower()
        if key not in self._renderers:
            raise KeyError(f"renderer not registered: {name}")
        return self._renderers[key]

    def names(self) -> list[str]:
        return sorted(self._renderers)


def default_registry(mood: str = "cinematic") -> RendererRegistry:
    registry = RendererRegistry()
    registry.register("ffmpeg_mvp", FfmpegMvpRenderer(mood=mood))
    return registry
