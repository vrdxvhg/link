"""Dependency-light audio analysis for the JARVIS song pipeline."""

from __future__ import annotations

import json
import math
import shutil
import subprocess
from pathlib import Path
from typing import Any


def probe_audio(audio_path: str) -> dict[str, Any]:
    """Return ffprobe-derived duration/sample metadata when ffprobe exists."""
    path = Path(audio_path)
    if not path.exists():
        raise FileNotFoundError(audio_path)

    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        return {"available": False, "duration_seconds": None, "sample_rate": None, "channels": None}

    command = [
        ffprobe, "-v", "error", "-select_streams", "a:0",
        "-show_entries", "stream=duration,sample_rate,channels",
        "-of", "json", str(path),
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout or "{}")
    stream = (data.get("streams") or [{}])[0]
    duration = stream.get("duration")
    return {
        "available": True,
        "duration_seconds": float(duration) if duration else None,
        "sample_rate": int(stream["sample_rate"]) if stream.get("sample_rate") else None,
        "channels": int(stream["channels"]) if stream.get("channels") else None,
    }


def estimate_scene_count(duration_seconds: float | None, bpm: float = 120.0) -> int:
    if not duration_seconds or duration_seconds <= 0:
        return 1
    beats = duration_seconds * bpm / 60.0
    return max(1, math.ceil(beats / 8.0))
