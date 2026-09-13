"""JARVIS V2 Security Center defensive automation facade."""
from __future__ import annotations

import datetime as dt
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOG = ROOT / "logs" / "security_center.log"

BLOCKED = (
    "format ", "diskpart", "cipher /w", "del /s", "rd /s", "rmdir /s",
    "shutdown", "reg delete", "schtasks /create", "net user", "mimikatz",
    "powershell -enc", "invoke-expression", "iex ", "downloadstring",
)

class SecurityCenter:
    """Local defensive Security Center automation facade."""

    def _log(self, action: str, **data: object) -> None:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with LOG.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps({
                "time": dt.datetime.now().isoformat(timespec="seconds"),
                "action": action,
                **data,
            }, ensure_ascii=False) + "\n")

    def open_terminal(self) -> str:
        """Open a normal local PowerShell window rooted at JARVIS."""
        subprocess.Popen(
            ["powershell.exe", "-NoExit"],
            cwd=str(ROOT.parent.parent),
            creationflags=getattr(subprocess, "CREATE_NEW_CONSOLE", 0),
        )
        self._log("open_terminal", cwd=str(ROOT.parent.parent))
        return "Security terminal opened"

    def run_local_command(self, command: str) -> tuple[int, str, str]:
        """Run an explicitly supplied local PowerShell command after policy checks."""
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

    def defensive_inventory(self, area: str) -> tuple[int, str, str]:
        """Run a predefined read-only local inventory for a Security Center area."""
        commands = {
            "network scanner": "Get-NetIPConfiguration | Format-List",
            "windows security": "Get-CimInstance Win32_OperatingSystem | Select-Object Caption,Version,BuildNumber",
            "linux security": "if (Get-Command wsl -ErrorAction SilentlyContinue) { wsl uname -a } else { 'WSL not installed' }",
            "log / soc monitor": "Get-WinEvent -ListLog * -ErrorAction SilentlyContinue | Select-Object -First 25 LogName,RecordCount,IsEnabled",
            "process inventory": "Get-Process | Sort-Object CPU -Descending | Select-Object -First 25 Name,Id,CPU",
            "service inventory": "Get-Service | Sort-Object Status,Name | Select-Object -First 50 Status,Name,DisplayName",
        }
        command = commands.get(area.lower())
        if not command:
            return 2, "", f"No predefined defensive inventory for: {area}"
        return self.run_local_command(command)

    def status(self) -> dict[str, str]:
        return {"module": "JARVIS Security Center", "status": "ready", "scope": "local/authorized"}

    def route_voice_command(self, text: str) -> tuple[bool, str]:
        """Handle safe Security Center voice commands."""
        raw = (text or "").strip()
        command = " ".join(raw.lower().split())
        if command in {"open security terminal", "security terminal kholo", "सिक्योरिटी टर्मिनल खोलो"}:
            return True, self.open_terminal()
        if command in {"security status", "सिक्योरिटी स्टेटस"}:
            return True, json.dumps(self.status(), ensure_ascii=False)

        inventory_prefixes = (
            "security scan ", "run security scan ", "सिक्योरिटी स्कैन ",
        )
        for prefix in inventory_prefixes:
            if command.startswith(prefix):
                area = raw[len(prefix):].strip()
                code, out, err = self.defensive_inventory(area)
                return True, (out or err or f"scan exited with code {code}").strip()

        prefixes = (
            "security command ", "run security command ", "सिक्योरिटी कमांड चलाओ ",
        )
        for prefix in prefixes:
            if command.startswith(prefix):
                raw_command = raw[len(prefix):].strip()
                code, out, err = self.run_local_command(raw_command)
                return True, (out or err or f"command exited with code {code}").strip()
        return False, ""
