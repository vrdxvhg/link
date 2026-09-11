"""End-to-end first-pass song-to-YouTube package builder for JARVIS V2."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    from .song_factory import build_song_project
    from .youtube_metadata import build_metadata
    from .thumbnail_generator import generate_thumbnail
    from .render_engine import render_song_video
    from .youtube_publish_flow import UploadPackage, prepare_upload
except ImportError:
    from song_factory import build_song_project
    from youtube_metadata import build_metadata
    from thumbnail_generator import generate_thumbnail
    from render_engine import render_song_video
    from youtube_publish_flow import UploadPackage, prepare_upload


def build_song_to_youtube(audio_path: str, output_dir: str = "workspace/projects", title: str | None = None,
                          bpm: float = 120.0, mood: str = "cinematic", language: str = "Hindi") -> dict[str, Any]:
    manifest = build_song_project(audio_path, output_dir, bpm, mood)
    project = Path(manifest["project_dir"])
    source = Path(audio_path)
    video_path = project / "final.mp4"
    thumbnail_path = project / "thumbnail.jpg"
    metadata_path = project / "youtube_metadata.json"

    final_title = title or source.stem.replace("_", " ")
    metadata = build_metadata(final_title, mood=mood, language=language)
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    if not video_path.exists():
        render_song_video(str(source), str(video_path))
    if not thumbnail_path.exists():
        generate_thumbnail(str(thumbnail_path), final_title)

    package = prepare_upload(UploadPackage(
        video=str(video_path), title=metadata["title"],
        description=metadata["description"], thumbnail=str(thumbnail_path), visibility="private"
    ))
    manifest["youtube_package"] = package.to_dict()
    manifest["status"] = "awaiting_human_approval"
    (project / "project.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Build a JARVIS V2 song-to-YouTube package")
    parser.add_argument("audio")
    parser.add_argument("--output", default="workspace/projects")
    parser.add_argument("--title")
    parser.add_argument("--bpm", type=float, default=120.0)
    parser.add_argument("--mood", default="cinematic")
    parser.add_argument("--language", default="Hindi")
    args = parser.parse_args()
    print(json.dumps(build_song_to_youtube(args.audio, args.output, args.title, args.bpm, args.mood, args.language), ensure_ascii=False, indent=2))
