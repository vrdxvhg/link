"""Local-first persistent job registry for JARVIS V2 YouTube Automation."""
from __future__ import annotations
import json
import os
import threading
import time
import uuid
from pathlib import Path
from typing import Any

JOBS_DIR = Path(os.getenv("JARVIS_JOBS", "workspace/jobs")).resolve()
JOBS_DIR.mkdir(parents=True, exist_ok=True)
_LOCK = threading.Lock()


def create_job(kind: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    job = {"id": uuid.uuid4().hex, "kind": kind, "status": "queued", "created_at": time.time(), "payload": payload or {}}
    _write(job)
    return job


def get_job(job_id: str) -> dict[str, Any] | None:
    path = (JOBS_DIR / f"{job_id}.json").resolve()
    if path.parent != JOBS_DIR or not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def update_job(job_id: str, **changes: Any) -> dict[str, Any]:
    with _LOCK:
        job = get_job(job_id)
        if job is None:
            raise FileNotFoundError(job_id)
        job.update(changes)
        job["updated_at"] = time.time()
        _write(job)
        return job


def _write(job: dict[str, Any]) -> None:
    path = JOBS_DIR / f"{job['id']}.json"
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(job, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)
