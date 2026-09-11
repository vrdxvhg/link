"""Local-first job registry for JARVIS V2 YouTube Automation."""
from __future__ import annotations
import json
import time
import uuid
from pathlib import Path
from typing import Any

JOBS_DIR = Path(__import__("os").getenv("JARVIS_JOBS", "workspace/jobs")).resolve()
JOBS_DIR.mkdir(parents=True, exist_ok=True)


def create_job(kind: str, payload: dict[str, Any]) -> dict[str, Any]:
    job = {"id": uuid.uuid4().hex, "kind": kind, "status": "queued", "created_at": time.time(), "payload": payload}
    (JOBS_DIR / f"{job['id']}.json").write_text(json.dumps(job, indent=2), encoding="utf-8")
    return job


def get_job(job_id: str) -> dict[str, Any] | None:
    path = JOBS_DIR / f"{job_id}.json"
    if path.parent != JOBS_DIR or not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def update_job(job_id: str, **changes: Any) -> dict[str, Any]:
    job = get_job(job_id)
    if job is None:
        raise FileNotFoundError(job_id)
    job.update(changes)
    (JOBS_DIR / f"{job_id}.json").write_text(json.dumps(job, indent=2), encoding="utf-8")
    return job
