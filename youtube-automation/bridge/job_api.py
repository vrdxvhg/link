"""Small bridge adapter for creating and starting song-to-YouTube jobs."""
from __future__ import annotations
try:
    from .jobs import create_job, get_job
    from .worker import submit_job
except ImportError:
    from jobs import create_job, get_job
    from worker import submit_job


def create_and_start_song_job(audio_path: str, output_dir: str = "workspace/projects", bpm: float = 120.0, mood: str = "cinematic") -> dict:
    job = create_job("song_to_youtube", {"audio_path": audio_path, "output_dir": output_dir, "bpm": bpm, "mood": mood})
    submit_job(job["id"])
    return get_job(job["id"]) or job
