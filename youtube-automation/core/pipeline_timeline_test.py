from pathlib import Path
import json

from pipeline_runner import _write_render_timeline


def test_render_timeline_persists_scene_and_beat_data(tmp_path: Path) -> None:
    manifest = {
        "scene_plan": {
            "duration_seconds": 12.5,
            "bpm": 120.0,
            "beat_seconds": 0.5,
            "beat_timeline": [0.0, 0.5, 1.0],
            "scenes": [{"index": 1, "start_seconds": 0.0, "end_seconds": 4.0}],
        }
    }
    path = _write_render_timeline(tmp_path, manifest)
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["duration_seconds"] == 12.5
    assert data["bpm"] == 120.0
    assert data["beat_timeline"] == [0.0, 0.5, 1.0]
    assert data["scenes"][0]["end_seconds"] == 4.0


if __name__ == "__main__":
    test_render_timeline_persists_scene_and_beat_data(Path("."))
    print("pipeline timeline tests: PASS")
