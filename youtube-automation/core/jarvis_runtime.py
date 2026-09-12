"""Backward-compatible runtime entry point for JARVIS V2.

`runtime.py` is the canonical coordinator. This module remains as a compatibility
shim for older callers that imported `jarvis_runtime.JarvisRuntime`.
"""
from __future__ import annotations

try:
    from .runtime import JarvisRuntime as _CanonicalRuntime
except ImportError:
    from runtime import JarvisRuntime as _CanonicalRuntime


class JarvisRuntime(_CanonicalRuntime):
    """Compatibility wrapper around the canonical runtime coordinator."""

    def start(self, microphone: bool = False):
        if microphone and self.listening and not self.microphone_running:
            self.start_microphone()
        return self.status()

    def stop(self):
        self.stop_microphone()
        return self.status()

    def handle_text(self, text: str):
        self.command(text)
        return self.status()


if __name__ == "__main__":
    runtime = JarvisRuntime()
    print(runtime.start())
    for phrase in ("deactivate system", "i am vikas", "lock", "deactivate system", "i am vikas"):
        print(phrase, "->", runtime.handle_text(phrase))
    runtime.stop()
