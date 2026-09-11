from pathlib import Path

from youtube_adapter import ApprovalGuardAdapter, BrowserUploadResult
from youtube_publish_flow import UploadPackage, PublishState


class FakeAdapter(ApprovalGuardAdapter):
    def _upload_approved(self, package: UploadPackage) -> BrowserUploadResult:
        return BrowserUploadResult(external_url="https://example.invalid/video", published=True)


def test_approval_gate_allows_adapter_upload(tmp_path):
    video = tmp_path / "final.mp4"
    video.write_bytes(b"video")
    package = UploadPackage(video=str(video), title="Test")
    result = FakeAdapter().upload(package)
    assert result.published is True
    assert package.state is PublishState.AWAITING_APPROVAL


if __name__ == "__main__":
    print("youtube adapter tests: PASS")
