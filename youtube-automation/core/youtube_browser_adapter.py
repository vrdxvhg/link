"""Browser adapter contract for YouTube Studio automation.

Core logic never drives a browser directly. An adapter is responsible for UI
interaction and must stop before public publishing until approval is explicit.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class BrowserUploadResult:
    video_id: Optional[str] = None
    url: Optional[str] = None
    status: str = "prepared"


class YouTubeBrowserAdapter(ABC):
    @abstractmethod
    def open_studio(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def select_video(self, video_path: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def fill_metadata(self, title: str, description: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_thumbnail(self, thumbnail_path: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_visibility(self, visibility: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def wait_for_human_approval(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def publish_or_schedule(self) -> BrowserUploadResult:
        raise NotImplementedError


class DryRunYouTubeAdapter(YouTubeBrowserAdapter):
    """Safe adapter used in local testing; performs no browser interaction."""

    def __init__(self, approved: bool = False) -> None:
        self.approved = approved
        self.actions: list[tuple[str, tuple[object, ...]]] = []

    def _record(self, action: str, *args: object) -> None:
        self.actions.append((action, args))

    def open_studio(self) -> None:
        self._record("open_studio")

    def select_video(self, video_path: str) -> None:
        self._record("select_video", video_path)

    def fill_metadata(self, title: str, description: str) -> None:
        self._record("fill_metadata", title, description)

    def set_thumbnail(self, thumbnail_path: str) -> None:
        self._record("set_thumbnail", thumbnail_path)

    def set_visibility(self, visibility: str) -> None:
        if visibility == "public" and not self.approved:
            raise PermissionError("public publishing requires explicit approval")
        self._record("set_visibility", visibility)

    def wait_for_human_approval(self) -> bool:
        return self.approved

    def publish_or_schedule(self) -> BrowserUploadResult:
        if not self.approved:
            raise PermissionError("publishing requires explicit human approval")
        self._record("publish_or_schedule")
        return BrowserUploadResult(status="dry_run_published")
