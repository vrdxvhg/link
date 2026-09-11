"""Background song-to-YouTube job runner for JARVIS V2."""
from __future__ import annotations
import threading
from pathlib import Path
from typing import Any

try:
    from .jobs import update_job
except ImportError:
    from jobs import update_job
try:
    from ..core.song_factory import build_song_project
except ImportError:
    from youtube_automation.core.song_factory import build_song_project


def run_song_job(job_id: str, audio_path: str, output_dir: str = "workspace/projects", bpm: float = 120.0, mood: str = "cinematic") -> None:
    try:
        update_job(job_id, status="running")
        manifest = build_song_project(audio_path, output_dir=output_dir, bpm=bpm, mood=mood)
        update_job(job_id, status="completed", result=manifest)
    except Exception as exc:
        update_job(job_id, status="failed", error=f"{type(exc).__name__}: {exc}")


def start_song_job(job_id: str, audio_path: str, **options: Any) -> threading.Thread:
    thread = threading.Thread(target=run_song_job, args=(job_id, audio_path), kwargs=options, daemon=True)
    thread.start()
    return thread
