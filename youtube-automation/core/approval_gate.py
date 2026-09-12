"""Human approval gate for JARVIS V2 publishing actions."""
from __future__ import annotations
from dataclasses import dataclass
import time


@dataclass
class ApprovalGate:
    approved: bool = False
    approved_at: float | None = None
    approved_by: str | None = None

    def approve(self, approver: str = "human") -> None:
        self.approved = True
        self.approved_at = time.time()
        self.approved_by = approver.strip() or "human"

    def revoke(self) -> None:
        self.approved = False
        self.approved_at = None
        self.approved_by = None

    def require(self) -> None:
        if not self.approved:
            raise PermissionError("human approval is required before publishing")

    def to_dict(self) -> dict[str, object]:
        return {
            "approved": self.approved,
            "approved_at": self.approved_at,
            "approved_by": self.approved_by,
        }
