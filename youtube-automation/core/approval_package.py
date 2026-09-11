"""Build an approval-ready artifact manifest for JARVIS V2."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any


def build_approval_package(project_dir: str) -> dict[str, Any]:
    root = Path(project_dir).resolve()
    project_file = root / "project.json"
    if not project_file.is_file():
        raise FileNotFoundError(str(project_file))
    manifest = json.loads(project_file.read_text(encoding="utf-8"))
    outputs = manifest.get("outputs", {})
    result = {"project_dir": str(root), "approval_required": True, "ready": True, "files": {}}
    for key, value in outputs.items():
        path = Path(value)
        result["files"][key] = {"path": str(path), "exists": path.is_file(), "size": path.stat().st_size if path.is_file() else 0}
        if not path.is_file():
            result["ready"] = False
    out = root / "approval_package.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return result
