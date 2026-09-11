"""JARVIS V2 Song -> Music Video planning engine.

This first implementation is intentionally dependency-light: it analyzes media metadata
through ffprobe/ffmpeg when available and produces a deterministic project manifest that
later renderers can consume.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


def probe_audio(path: str) -> dict[str, Any]:
    """Return basic audio metadata using ffprobe when installed."""
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration:stream=codec_name,sample_rate,channels",
        "-of", "json", path,
    ]
    try:
        raw = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
        return json.loads(raw)
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError):
        return {"format": {}, "streams": [], "probe_error": "ffprobe unavailable or input unreadable"}


def build_song_project(audio_path: str, output_dir: str = "workspace/projects") -> dict[str, Any]:
    """Create a reusable manifest for a song-driven cinematic/3D video."""
    source = Path(audio_path)
    project_name = source.stem.replace(" ", "_")
    project_dir = Path(output_dir) / project_name
    project_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "version": "2.0",
        "type": "song_to_youtube",
        "source_audio": str(source),
        "project_dir": str(project_dir),
        "analysis": probe_audio(str(source)),
        "visual_direction": {
            "style": "cinematic_3d",
            "beat_sync": True,
            "lyrics_sync": True,
            "mood_adaptive": True,
            "scene_changes_on_beats": True,
            "aspect_ratio": "16:9",
            "resolution": "1920x1080",
        },
        "outputs": {
            "video": str(project_dir / "final.mp4"),
            "thumbnail": str(project_dir / "thumbnail.jpg"),
            "metadata": str(project_dir / "youtube_metadata.json"),
        },
        "publish": {
            "approval_required": True,
            "visibility": "private",
        },
    }
    (project_dir / "project.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Create a JARVIS V2 song video project manifest")
    parser.add_argument("audio")
    parser.add_argument("--output", default="workspace/projects")
    args = parser.parse_args()
    print(json.dumps(build_song_project(args.audio, args.output), indent=2))
