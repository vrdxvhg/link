"""Safe YouTube Studio publishing state machine for JARVIS V2."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Optional

from .approval_gate import ApprovalGate


class PublishState(str, Enum):
    READY = "ready"
    VIDEO_SELECTED = "video_selected"
    METADATA_READY = "metadata_ready"
    THUMBNAIL_READY = "thumbnail_ready"
    UPLOAD_READY = "upload_ready"
    AWAITING_APPROVAL = "awaiting_approval"
    PUBLISHED = "published"


@dataclass
class UploadPackage:
    video: str
    title: str
    description: str = ""
    thumbnail: Optional[str] = None
    visibility: str = "private"
    state: PublishState = PublishState.READY
    approval: ApprovalGate | None = None

    def validate(self) -> None:
        if not Path(self.video).is_file():
            raise FileNotFoundError(self.video)
        if not self.title.strip():
            raise ValueError("title is required")
        if self.thumbnail and not Path(self.thumbnail).is_file():
            raise FileNotFoundError(self.thumbnail)
        if self.visibility not in {"private", "unlisted", "public"}:
            raise ValueError("visibility must be private, unlisted, or public")

    def to_dict(self) -> dict:
        data = asdict(self)
        data["state"] = self.state.value
        data["approval"] = self.approval.to_dict() if self.approval else None
        return data

    def mark_video_selected(self) -> "UploadPackage":
        self.validate()
        self.state = PublishState.VIDEO_SELECTED
        return self

    def mark_metadata_ready(self) -> "UploadPackage":
        self.validate()
        self.state = PublishState.METADATA_READY
        return self

    def mark_thumbnail_ready(self) -> "UploadPackage":
        self.validate()
        self.state = PublishState.THUMBNAIL_READY
        return self


def prepare_upload(package: UploadPackage) -> UploadPackage:
    package.validate()
    package.state = PublishState.UPLOAD_READY
    return package


def approve_for_publish(package: UploadPackage, approver: str = "human") -> UploadPackage:
    """Require explicit human approval before the adapter may publish."""
    package.validate()
    package.approval = package.approval or ApprovalGate()
    package.approval.approve(approver)
    package.state = PublishState.AWAITING_APPROVAL
    return package


def mark_published(package: UploadPackage) -> UploadPackage:
    package.validate()
    if package.approval is None:
        raise PermissionError("human approval is required before publishing")
    package.approval.require()
    package.state = PublishState.PUBLISHED
    return package
