"""Pure orchestration tests; renderer dependencies are patched in real integration runs."""
from pathlib import Path


def test_upload_contract_is_private_by_default():
    # Contract test kept dependency-light: public publishing is never the default.
    from youtube_publish_flow import UploadPackage, PublishState
    package = UploadPackage(video="x.mp4", title="Demo")
    assert package.visibility == "private"
    assert package.state is PublishState.READY


def test_project_output_names_are_stable(tmp_path: Path):
    from youtube_metadata import build_metadata
    data = build_metadata("Mitti Di Fasal", mood="village")
    assert data["title"] == "Mitti Di Fasal"
    assert "Music Video" in data["description"]
    assert "village" in data["tags"]


if __name__ == "__main__":
    test_upload_contract_is_private_by_default()
    test_project_output_names_are_stable(Path("."))
    print("song-to-youtube tests: PASS")
