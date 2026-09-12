"""End-to-end local pipeline runner for JARVIS V2 YouTube Automation."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .song_factory import build_song_project
from .render_engine import render_song_video
from .youtube_metadata import write_metadata
from .thumbnail_generator import generate_thumbnail


def _write_render_timeline(project_dir: Path, manifest: dict[str, Any]) -> Path:
    """Persist the planned beat/scene timeline for downstream renderers and UI."""
    scene_plan = manifest.get("scene_plan", {})
    timeline = {
        "version": "1.0",
        "duration_seconds": scene_plan.get("duration_seconds"),
        "bpm": scene_plan.get("bpm"),
        "beat_seconds": scene_plan.get("beat_seconds"),
        "beat_timeline": scene_plan.get("beat_timeline", []),
        "scenes": scene_plan.get("scenes", []),
    }
    path = project_dir / "render_timeline.json"
    path.write_text(json.dumps(timeline, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def run_pipeline(
    audio_path: str,
    output_dir: str = "workspace/projects",
    bpm: float = 120.0,
    mood: str = "cinematic",
    title: str | None = None,
) -> dict[str, Any]:
    manifest = build_song_project(audio_path, output_dir=output_dir, bpm=bpm, mood=mood)
    project_dir = Path(manifest["project_dir"])
    title = title or Path(audio_path).stem.replace("_", " ")
    video_path = project_dir / "final.mp4"
    thumbnail_path = project_dir / "thumbnail.jpg"

    timeline_path = _write_render_timeline(project_dir, manifest)
    render_song_video(audio_path, str(video_path), mood=mood)
    write_metadata(str(project_dir), title, mood=mood)
    generate_thumbnail(str(thumbnail_path), title)

    manifest["outputs"].update(
        {
            "video": str(video_path),
            "thumbnail": str(thumbnail_path),
            "metadata": str(project_dir / "youtube_metadata.json"),
            "render_timeline": str(timeline_path),
        }
    )
    manifest["publish"]["state"] = "awaiting_approval"
    (project_dir / "project.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return manifest
