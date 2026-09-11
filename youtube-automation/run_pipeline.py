"""CLI launcher for the JARVIS V2 local song-to-YouTube pipeline."""
from __future__ import annotations

import argparse
import json

from youtube_automation.core.pipeline_runner import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the JARVIS V2 song-to-YouTube pipeline")
    parser.add_argument("audio")
    parser.add_argument("--output", default="workspace/projects")
    parser.add_argument("--bpm", type=float, default=120.0)
    parser.add_argument("--mood", default="cinematic")
    parser.add_argument("--title")
    args = parser.parse_args()
    result = run_pipeline(args.audio, args.output, args.bpm, args.mood, args.title)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
