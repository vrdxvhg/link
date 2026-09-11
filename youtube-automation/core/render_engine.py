"""FFmpeg MVP renderer for song-driven cinematic videos."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def _color_for_mood(mood: str) -> str:
    palette = {
        "romantic": "0x3a1028",
        "sad": "0x101b2f",
        "devotional": "0x3a2a10",
        "energetic": "0x1d1038",
        "punjabi": "0x32150a",
        "village": "0x172514",
    }
    return palette.get(mood.lower(), "0x111827")


def render_song_video(
    audio_path: str,
    output_path: str,
    width: int = 1920,
    height: int = 1080,
    fps: int = 30,
    mood: str = "cinematic",
) -> str:
    audio = Path(audio_path)
    output = Path(output_path)
    if not audio.exists():
        raise FileNotFoundError(audio_path)
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("FFmpeg is required to render JARVIS videos.")
    output.parent.mkdir(parents=True, exist_ok=True)

    base = _color_for_mood(mood)
    # Subtle animated zoom plus vignette creates a usable cinematic MVP while
    # preserving a clean adapter point for the future 3D scene renderer.
    filter_graph = (
        f"color=c={base}:s={width}x{height}:r={fps},"
        "zoompan=z='min(zoom+0.0005,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s="
        f"{width}x{height}:fps={fps},"
        "vignette=PI/5,format=yuv420p"
    )
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
    parser.add_argument("--mood", default="cinematic")
    args = parser.parse_args()
    print(render_song_video(args.audio, args.output, mood=args.mood))
