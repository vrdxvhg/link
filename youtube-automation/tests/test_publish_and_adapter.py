from pathlib import Path

from youtube_automation.core.approval_gate import ApprovalGate
from youtube_automation.core.youtube_browser_adapter import DryRunYouTubeAdapter
from youtube_automation.core.youtube_publish_flow import UploadPackage, approve_for_publish, mark_published, prepare_upload


def test_public_publish_requires_approval(tmp_path: Path) -> None:
    video = tmp_path / "video.mp4"
    thumb = tmp_path / "thumb.jpg"
    video.write_bytes(b"mp4")
    thumb.write_bytes(b"jpg")
    adapter = DryRunYouTubeAdapter(approved=False)
    package = UploadPackage(str(video), "Test", thumbnail=str(thumb), visibility="public")
    prepare_upload(package)
    try:
        adapter.set_visibility("public")
    except PermissionError:
        pass
    else:
        raise AssertionError("public visibility must require approval")


def test_approval_unlocks_publish(tmp_path: Path) -> None:
    video = tmp_path / "video.mp4"
    video.write_bytes(b"mp4")
    package = UploadPackage(str(video), "Test", visibility="private")
    gate = ApprovalGate()
    assert gate.approved is False
    approve_for_publish(package, "tester")
    assert package.approval is not None
    assert package.approval.approved is True
    package.visibility = "public"
    adapter = DryRunYouTubeAdapter(approved=True)
    adapter.open_studio()
    adapter.select_video(str(video))
    adapter.fill_metadata(package.title, package.description)
    adapter.set_visibility("public")
    result = adapter.publish_or_schedule()
    assert result.status == "dry_run_published"
    mark_published(package)
    assert package.state.value == "published"
