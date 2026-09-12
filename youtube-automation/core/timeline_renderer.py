"""Deterministic FFmpeg timeline renderer for JARVIS V2 media plans."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Iterable

from .shorts_media_adapters import ShortSegment


def _run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def render_timeline(
    segments: Iterable[ShortSegment],
    output_path: str,
    *,
    width: int = 1920,
    height: int = 1080,
    fps: int = 30,
) -> str:
    """Render ordered local image/video segments into one MP4.

    Missing media is represented by a generated black clip, so a plan can be
    rendered deterministically before every stock asset is available.
    """
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("FFmpeg is required to render a JARVIS timeline.")
    items = list(segments)
    if not items:
        raise ValueError("at least one segment is required")
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    inputs: list[str] = []
    filters: list[str] = []
    concat_labels: list[str] = []
    for i, segment in enumerate(items):
        duration = max(float(segment.duration_seconds), 0.1)
        media = Path(segment.media_path) if segment.media_path else None
        if media and media.is_file():
            inputs += ["-stream_loop", "-1", "-i", str(media)]
            filters.append(
                f"[{i}:v]scale={width}:{height}:force_original_aspect_ratio=decrease," 
                f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,"
                f"fps={fps},trim=duration={duration},setpts=PTS-STARTPTS[v{i}]"
            )
        else:
            inputs += ["-f", "lavfi", "-t", str(duration), "-i", f"color=c=black:s={width}x{height}:r={fps}"]
            filters.append(f"[{i}:v]setpts=PTS-STARTPTS[v{i}]")
        concat_labels.append(f"[v{i}]")

    filters.append("".join(concat_labels) + f"concat=n={len(items)}:v=1:a=0[outv]")
    command = ["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(filters), "-map", "[outv]", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", str(output)]
    _run(command)
    return str(output)
