from pathlib import Path

from pipeline_runner import run_pipeline


def test_pipeline_requires_source(tmp_path):
    missing = tmp_path / "missing.mp3"
    try:
        run_pipeline(str(missing), output_dir=str(tmp_path / "projects"))
    except FileNotFoundError:
        return
    raise AssertionError("missing source must fail")


if __name__ == "__main__":
    test_pipeline_requires_source(Path("."))
    print("pipeline tests: PASS")
