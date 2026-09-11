"""Deterministic YouTube metadata and thumbnail-card generation helpers."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any


def build_metadata(title: str, mood: str = "cinematic", language: str = "Hindi") -> dict[str, Any]:
    clean = title.strip() or "JARVIS Music Video"
    return {
        "title": clean,
        "description": f"Official music video for {clean}. Created with the JARVIS V2 song-to-video pipeline.",
        "tags": [clean, "music video", "official", mood, language, "JARVIS V2"],
        "language": language,
        "category": "Music",
    }


def write_metadata(project_dir: str, title: str, mood: str = "cinematic", language: str = "Hindi") -> str:
    path = Path(project_dir) / "youtube_metadata.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build_metadata(title, mood, language), ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)
