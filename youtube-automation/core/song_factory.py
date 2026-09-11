"""JARVIS V2 Song -> Music Video project factory."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    from .audio_analyzer import probe_audio
    from .scene_planner import build_scene_plan
except ImportError:
    from audio_analyzer import probe_audio
    from scene_planner import build_scene_plan


def build_song_project(audio_path: str, output_dir: str = "workspace/projects", bpm: float = 120.0, mood: str = "cinematic") -> dict[str, Any]:
    source = Path(audio_path)
    if not source.exists():
        raise FileNotFoundError(audio_path)
    project_dir = Path(output_dir) / source.stem.replace(" ", "_")
    project_dir.mkdir(parents=True, exist_ok=True)
    analysis = probe_audio(str(source))
    duration = analysis.get("duration_seconds")
    scene_plan = build_scene_plan(duration or 1.0, bpm=bpm, mood=mood)
    manifest = {
        "version": "2.1",
        "type": "song_to_youtube",
        "source_audio": str(source),
        "project_dir": str(project_dir),
        "analysis": analysis,
        "scene_plan": scene_plan,
        "visual_direction": {"style": "cinematic_3d", "beat_sync": True, "lyrics_sync": True, "mood_adaptive": True, "aspect_ratio": "16:9", "resolution": "1920x1080"},
        "outputs": {"video": str(project_dir / "final.mp4"), "thumbnail": str(project_dir / "thumbnail.jpg"), "metadata": str(project_dir / "youtube_metadata.json")},
        "publish": {"approval_required": True, "visibility": "private"},
    }
    (project_dir / "project.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (project_dir / "scene_plan.json").write_text(json.dumps(scene_plan, indent=2), encoding="utf-8")
    return manifest


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Create a JARVIS V2 song video project")
    parser.add_argument("audio")
    parser.add_argument("--output", default="workspace/projects")
    parser.add_argument("--bpm", type=float, default=120.0)
    parser.add_argument("--mood", default="cinematic")
    args = parser.parse_args()
    print(json.dumps(build_song_project(args.audio, args.output, args.bpm, args.mood), indent=2))
