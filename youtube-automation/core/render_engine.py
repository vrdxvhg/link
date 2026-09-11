"""FFmpeg MVP renderer: creates a real MP4 from a song and a generated visual background."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def render_song_video(audio_path: str, output_path: str, width: int = 1920, height: int = 1080, fps: int = 30) -> str:
    audio = Path(audio_path)
    output = Path(output_path)
    if not audio.exists():
        raise FileNotFoundError(audio_path)
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("FFmpeg is required to render JARVIS videos.")
    output.parent.mkdir(parents=True, exist_ok=True)
    # Deterministic cinematic gradient background; later scene renderers replace this source.
    filter_graph = f"color=c=black:s={width}x{height}:r={fps},format=yuv420p"
    command = [
        "ffmpeg", "-y", "-f", "lavfi", "-i", filter_graph,
        "-i", str(audio), "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k", "-shortest", str(output),
    ]
    subprocess.run(command, check=True)
    return str(output)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("audio")
    parser.add_argument("output")
    args = parser.parse_args()
    print(render_song_video(args.audio, args.output))
