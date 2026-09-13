"""JARVIS V2 Security Center command/terminal automation.

This layer is intentionally limited to local, user-supplied, defensive
commands. It provides a bridge for the existing JARVIS voice runtime without
embedding offensive tooling or unauthorized-access automation.
"""
from __future__ import annotations

import datetime as dt
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOG = ROOT / "logs" / "security_center.log"

# Refuse common destructive, credential-theft, persistence, and encoded-payload
# patterns in the voice automation layer. Approved security tools can later be
# wrapped behind explicit scope/approval checks.
BLOCKED = (
    "format ", "diskpart", "cipher /w", "del /s", "rd /s", "rmdir /s",
    "shutdown", "reg delete", "schtasks /create", "net user", "mimikatz",
    "powershell -enc", "invoke-expression", "iex ", "downloadstring",
)

class SecurityCenter:
    """Local Security Center automation facade."""

    def _log(self, action: str, **data: object) -> None:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with LOG.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps({
                "time": dt.datetime.now().isoformat(timespec="seconds"),
                "action": action,
                **data,
            }, ensure_ascii=False) + "\n")

    def open_terminal(self) -> str:
        """Open a normal local PowerShell window rooted at the project."""
        subprocess.Popen(
            ["powershell.exe", "-NoExit"],
            cwd=str(ROOT.parent.parent),
            creationflags=getattr(subprocess, "CREATE_NEW_CONSOLE", 0),
        )
        self._log("open_terminal", cwd=str(ROOT.parent.parent))
        return "Security terminal opened"

    def run_local_command(self, command: str) -> tuple[int, str, str]:
        """Run an explicitly supplied local PowerShell command."""
        command = command.strip()
        if not command:
            return 2, "", "No command supplied"
        lowered = command.lower()
        if any(token in lowered for token in BLOCKED):
            self._log("blocked_command", command=command)
            return 3, "", "Command blocked by Security Center safety policy"

        self._log("run_command", command=command)
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-Command", command],
            cwd=str(ROOT.parent.parent), text=True, capture_output=True,
        )
        return result.returncode, result.stdout, result.stderr

    def status(self) -> dict[str, str]:
        return {"module": "JARVIS Security Center", "status": "ready", "scope": "local/authorized"}

    def route_voice_command(self, text: str) -> tuple[bool, str]:
        """Handle a small safe command vocabulary from JARVIS voice input."""
        command = " ".join((text or "").lower().strip().split())
        if command in {"open security terminal", "security terminal kholo", "सिक्योरिटी टर्मिनल खोलो"}:
            return True, self.open_terminal()
        if command in {"security status", "सिक्योरिटी स्टेटस"}:
            return True, json.dumps(self.status(), ensure_ascii=False)

        prefixes = (
            "security command ",
            "run security command ",
            "सिक्योरिटी कमांड चलाओ ",
        )
        for prefix in prefixes:
            if command.startswith(prefix):
                raw = text.strip()[len(prefix):].strip()
                code, out, err = self.run_local_command(raw)
                return True, (out or err or f"command exited with code {code}").strip()
        return False, ""
