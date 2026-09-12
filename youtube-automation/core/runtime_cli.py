"""Small CLI smoke/demo for the JARVIS V2 runtime coordinator."""
from __future__ import annotations

import argparse

try:
    from .runtime import JarvisRuntime
except ImportError:
    from runtime import JarvisRuntime


def main() -> int:
    parser = argparse.ArgumentParser(description="JARVIS V2 runtime command demo")
    parser.add_argument("commands", nargs="*", help="commands to route through VoiceControl")
    args = parser.parse_args()

    runtime = JarvisRuntime(on_ui_state=lambda state: print(f"UI state: {state}"))
    print("Runtime:", runtime.status())

    for text in args.commands:
        state = runtime.command(text)
        print(f"> {text}\n  state={state} status={runtime.status()}")

    runtime.stop_microphone()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
