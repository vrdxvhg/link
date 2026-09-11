"""FFmpeg-based thumbnail generator for JARVIS song projects."""
from __future__ import annotations
import shutil
import subprocess
from pathlib import Path


def generate_thumbnail(output_path: str, title: str) -> str:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("FFmpeg is required to generate thumbnails.")
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    text = title.replace(":", "\\:").replace("'", "\\'")[:60]
    vf = "drawtext=text='" + text + "':fontcolor=white:fontsize=72:x=(w-text_w)/2:y=(h-text_h)/2"
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=1280x720", "-vf", vf, "-frames:v", "1", str(output)], check=True)
    return str(output)
