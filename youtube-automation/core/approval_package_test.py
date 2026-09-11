from approval_package import build_approval_package
import json


def test_approval_package_reports_missing_outputs(tmp_path):
    root = tmp_path / "project"
    root.mkdir()
    (root / "project.json").write_text(json.dumps({"outputs": {"video": str(root / "final.mp4"), "thumbnail": str(root / "thumbnail.jpg"), "metadata": str(root / "youtube_metadata.json")}}), encoding="utf-8")
    result = build_approval_package(str(root))
    assert result["approval_required"] is True
    assert result["ready"] is False


if __name__ == "__main__":
    print("approval package tests: PASS")
