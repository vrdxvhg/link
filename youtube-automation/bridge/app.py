"""Minimal local-first HTTP bridge for JARVIS V2 YouTube Automation."""
from __future__ import annotations
import os
import re
from pathlib import Path
from urllib.parse import quote
from flask import Flask, jsonify, request, send_file
try:
    from .jobs import create_job, get_job, update_job
    from .worker import submit_job
except ImportError:
    from jobs import create_job, get_job, update_job
    from worker import submit_job
try:
    from ..core.ui_runtime import JARVISUIRuntime
except ImportError:
    try:
        from youtube_automation.core.ui_runtime import JARVISUIRuntime
    except ImportError:
        JARVISUIRuntime = None

MAX_UPLOAD_BYTES = int(os.getenv("JARVIS_MAX_UPLOAD_BYTES", str(2 * 1024 * 1024 * 1024)))
WORKSPACE = Path(os.getenv("JARVIS_WORKSPACE", "workspace/uploads")).resolve()
TOKEN = os.getenv("JARVIS_BRIDGE_TOKEN", "")
NAME_RE = re.compile(r"[^A-Za-z0-9._ -]")
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_BYTES
WORKSPACE.mkdir(parents=True, exist_ok=True)
UI_RUNTIME = JARVISUIRuntime() if JARVISUIRuntime is not None else None


def authorized() -> bool:
    return not TOKEN or request.headers.get("Authorization", "") == f"Bearer {TOKEN}"


def safe_name(name: str) -> str:
    cleaned = NAME_RE.sub("_", Path(name).name).strip(" .")
    if not cleaned:
        raise ValueError("invalid filename")
    return cleaned[:180]


def files() -> list[Path]:
    return sorted((p for p in WORKSPACE.iterdir() if p.is_file()), key=lambda p: p.name.lower())


@app.before_request
def auth_gate():
    if request.path == "/health":
        return None
    if not authorized():
        return jsonify({"error": "unauthorized"}), 401
    return None


@app.get("/health")
def health():
    return jsonify({"ok": True, "service": "jarvis-v2-bridge", "workspace": str(WORKSPACE)})


@app.get("/api/v1/ui/state")
def ui_state():
    if UI_RUNTIME is None:
        return jsonify({"error": "ui runtime unavailable"}), 503
    return jsonify(UI_RUNTIME.status())


@app.post("/api/v1/ui/command")
def ui_command():
    if UI_RUNTIME is None:
        return jsonify({"error": "ui runtime unavailable"}), 503
    data = request.get_json(silent=True) or {}
    command = str(data.get("command", "")).strip()
    if not command:
        return jsonify({"error": "command is required"}), 400
    try:
        state = UI_RUNTIME.command(command)
        return jsonify({"state": state, "ui": UI_RUNTIME.status()})
    except Exception as exc:
        return jsonify({"error": f"{type(exc).__name__}: {exc}"}), 400


@app.post("/api/v1/files/upload")
def upload():
    if "file" not in request.files:
        return jsonify({"error": "multipart field 'file' is required"}), 400
    incoming = request.files["file"]
    try:
        name = safe_name(incoming.filename or "")
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    target = WORKSPACE / name
    stem, suffix = target.stem, target.suffix
    index = 1
    while target.exists():
        target = WORKSPACE / f"{stem}_{index}{suffix}"
        index += 1
    incoming.save(target)
    return jsonify({"id": target.name, "name": target.name, "size": target.stat().st_size, "download": f"/api/v1/files/{quote(target.name)}/download"}), 201


@app.get("/api/v1/files")
def list_files():
    return jsonify({"files": [{"id": p.name, "name": p.name, "size": p.stat().st_size} for p in files()]})


@app.get("/api/v1/files/<path:file_id>")
def file_info(file_id: str):
    try:
        name = safe_name(file_id)
    except ValueError:
        return jsonify({"error": "invalid file id"}), 400
    path = (WORKSPACE / name).resolve()
    if path.parent != WORKSPACE or not path.is_file():
        return jsonify({"error": "file not found"}), 404
    return jsonify({"id": name, "name": name, "size": path.stat().st_size, "download": f"/api/v1/files/{quote(name)}/download"})


@app.get("/api/v1/files/<path:file_id>/download")
def download(file_id: str):
    try:
        name = safe_name(file_id)
    except ValueError:
        return jsonify({"error": "invalid file id"}), 400
    path = (WORKSPACE / name).resolve()
    if path.parent != WORKSPACE or not path.is_file():
        return jsonify({"error": "file not found"}), 404
    return send_file(path, as_attachment=True, download_name=path.name)


@app.post("/api/v1/jobs")
def create_job_route():
    data = request.get_json(silent=True) or {}
    kind = str(data.get("kind", "song_to_youtube")).strip()
    payload = data.get("payload") or {}
    if not kind or not isinstance(payload, dict):
        return jsonify({"error": "kind and object payload are required"}), 400
    job = create_job(kind, payload)
    if kind == "song_to_youtube" and (payload.get("audio_path") or payload.get("file_path")):
        submit_job(job["id"])
    return jsonify(job), 201


@app.get("/api/v1/jobs/<job_id>")
def get_job_route(job_id: str):
    job = get_job(job_id)
    return jsonify(job) if job else (jsonify({"error": "job not found"}), 404)


@app.post("/api/v1/jobs/<job_id>/status")
def update_job_route(job_id: str):
    data = request.get_json(silent=True) or {}
    status = str(data.get("status", "")).strip()
    if status not in {"queued", "running", "completed", "failed", "awaiting_approval"}:
        return jsonify({"error": "invalid status"}), 400
    try:
        return jsonify(update_job(job_id, status=status)), 200
    except FileNotFoundError:
        return jsonify({"error": "job not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("JARVIS_BRIDGE_PORT", "8787")))
