"""Browser automation contract for YouTube Studio.

The core pipeline never drives a browser directly. An adapter can implement the
UI-specific steps while the approval gate stays inside the domain model.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from .youtube_publish_flow import UploadPackage, PublishState, approve_for_publish


@dataclass
class BrowserUploadResult:
    external_url: str | None = None
    published: bool = False


class YouTubeStudioAdapter(ABC):
    @abstractmethod
    def upload(self, package: UploadPackage) -> BrowserUploadResult:
        """Upload only after the package has reached the approval gate."""
        raise NotImplementedError


class ApprovalGuardAdapter(YouTubeStudioAdapter):
    """Base adapter that requires an explicit approval transition."""

    def upload(self, package: UploadPackage) -> BrowserUploadResult:
        package = approve_for_publish(package)
        if package.state is not PublishState.AWAITING_APPROVAL:
            raise RuntimeError("YouTube upload blocked: approval gate not reached")
        return self._upload_approved(package)

    @abstractmethod
    def _upload_approved(self, package: UploadPackage) -> BrowserUploadResult:
        raise NotImplementedError
