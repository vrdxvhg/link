"""Background worker that executes JARVIS V2 song-to-YouTube jobs locally."""
from __future__ import annotations
import threading
from typing import Any
try:
    from .jobs import get_job, update_job
except ImportError:
    from jobs import get_job, update_job
try:
    from ..core.pipeline_runner import run_pipeline
except ImportError:
    from youtube_automation.core.pipeline_runner import run_pipeline


def run_job(job_id: str) -> dict:
    job = get_job(job_id)
    if not job:
        raise FileNotFoundError(job_id)
    update_job(job_id, status="running")
    try:
        payload = job.get("payload", {})
        audio_path = payload.get("audio_path") or payload.get("file_path")
        if not audio_path:
            raise ValueError("payload.audio_path is required")
        manifest = run_pipeline(
            audio_path,
            output_dir=payload.get("output_dir", "workspace/projects"),
            bpm=float(payload.get("bpm", 120.0)),
            mood=str(payload.get("mood", "cinematic")),
            title=payload.get("title"),
        )
        return update_job(job_id, status="awaiting_approval", result=manifest)
    except Exception as exc:
        return update_job(job_id, status="failed", error=f"{type(exc).__name__}: {exc}")


def submit_job(job_id: str) -> threading.Thread:
    thread = threading.Thread(target=run_job, args=(job_id,), name=f"jarvis-job-{job_id[:8]}", daemon=True)
    thread.start()
    return thread


def run_song_job(job_id: str, audio_path: str, output_dir: str = "workspace/projects", bpm: float = 120.0, mood: str = "cinematic", title: str | None = None) -> None:
    payload = {"audio_path": audio_path, "output_dir": output_dir, "bpm": bpm, "mood": mood, "title": title}
    update_job(job_id, payload=payload)
    run_job(job_id)


def start_song_job(job_id: str, audio_path: str, **options: Any) -> threading.Thread:
    thread = threading.Thread(target=run_song_job, args=(job_id, audio_path), kwargs=options, daemon=True)
    thread.start()
    return thread
