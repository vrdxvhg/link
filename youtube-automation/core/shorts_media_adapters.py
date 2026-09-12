"""Optional media adapters inspired by the JARVIS_TEST_01 source library.

These adapters keep the existing JARVIS V2 core independent from any one
third-party project. They provide small, testable contracts for Shorts-style
script, voice, stock footage and render stages without importing the original
projects wholesale.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable, Protocol


@dataclass(frozen=True)
class ShortSegment:
    """One ordered visual/audio segment in a Shorts timeline."""

    label: str
    text: str
    duration_seconds: float
    media_path: str | None = None


class ScriptProvider(Protocol):
    def generate(self, topic: str) -> dict: ...


class VoiceProvider(Protocol):
    def synthesize(self, text: str, output_path: str) -> str: ...


class FootageProvider(Protocol):
    def search(self, query: str, *, vertical: bool = True) -> str | None: ...


class RenderProvider(Protocol):
    def render(self, segments: Iterable[ShortSegment], output_path: str) -> str: ...


@dataclass
class ShortsMediaPlan:
    """Validated intermediate representation for an optional Shorts job."""

    topic: str
    segments: list[ShortSegment] = field(default_factory=list)
    title: str = ""
    description: str = ""
    tags: list[str] = field(default_factory=list)

    def validate(self) -> None:
        if not self.topic.strip():
            raise ValueError("topic is required")
        if not self.segments:
            raise ValueError("at least one segment is required")
        if any(segment.duration_seconds <= 0 for segment in self.segments):
            raise ValueError("segment duration must be positive")

    @property
    def duration_seconds(self) -> float:
        return sum(segment.duration_seconds for segment in self.segments)


def build_short_plan(
    topic: str,
    script: dict,
    *,
    footage_provider: FootageProvider | None = None,
) -> ShortsMediaPlan:
    """Convert a source-style Shorts script into a JARVIS-native media plan."""
    sections: list[tuple[str, str]] = []
    if script.get("intro"):
        sections.append(("intro", str(script["intro"])))
    for index, point in enumerate(script.get("points", []), start=1):
        heading = str(point.get("heading", "")).strip()
        body = str(point.get("body", "")).strip()
        text = ". ".join(part for part in (heading, body) if part)
        if text:
            sections.append((f"point_{index}", text))
    if script.get("outro"):
        sections.append(("outro", str(script["outro"])))

    segments: list[ShortSegment] = []
    for label, text in sections:
        # Source projects generally derive exact timing from generated audio.
        # Until a TTS result exists, use a conservative speech-rate estimate.
        duration = max(1.0, len(text.split()) / 2.15)
        media_path = None
        if footage_provider is not None:
            media_path = footage_provider.search(text, vertical=True)
        segments.append(ShortSegment(label, text, duration, media_path))

    plan = ShortsMediaPlan(
        topic=topic,
        segments=segments,
        title=str(script.get("title", topic)),
        description=str(script.get("description", "")),
        tags=[str(tag) for tag in script.get("tags", [])],
    )
    plan.validate()
    return plan


def render_with_provider(
    plan: ShortsMediaPlan,
    renderer: Callable[[Iterable[ShortSegment], str], str],
    output_path: str,
) -> str:
    """Render a validated plan through the selected JARVIS media renderer."""
    plan.validate()
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    return renderer(plan.segments, output_path)
