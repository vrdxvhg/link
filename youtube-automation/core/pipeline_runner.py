"""End-to-end local pipeline runner for JARVIS V2 YouTube Automation."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .song_factory import build_song_project
from .render_engine import render_song_video
from .youtube_metadata import write_metadata
from .thumbnail_generator import generate_thumbnail


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

    render_song_video(audio_path, str(video_path), mood=mood)
    write_metadata(str(project_dir), title, mood=mood)
    generate_thumbnail(str(thumbnail_path), title)

    manifest["outputs"].update(
        {
            "video": str(video_path),
            "thumbnail": str(thumbnail_path),
            "metadata": str(project_dir / "youtube_metadata.json"),
        }
    )
    manifest["publish"]["state"] = "awaiting_approval"
    (project_dir / "project.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return manifest
