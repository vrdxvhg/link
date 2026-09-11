"""Safe YouTube Studio publishing state machine for JARVIS V2.

The automation layer prepares the upload package and stops at an explicit approval gate.
Browser/UI automation can be attached later without coupling the core to a browser driver.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Optional


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
        return data


def prepare_upload(package: UploadPackage) -> UploadPackage:
    package.validate()
    package.state = PublishState.UPLOAD_READY
    return package


def approve_for_publish(package: UploadPackage) -> UploadPackage:
    """Explicit human approval transition; browser automation should only proceed after this."""
    package.validate()
    package.state = PublishState.AWAITING_APPROVAL
    return package
