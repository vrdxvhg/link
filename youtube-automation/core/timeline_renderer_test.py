from pathlib import Path

import pytest

from timeline_renderer import render_timeline
from shorts_media_adapters import ShortSegment


def test_empty_timeline_rejected(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        render_timeline([], str(tmp_path / "out.mp4"))


def test_missing_media_is_valid_input(tmp_path: Path) -> None:
    # The renderer should only fail here if FFmpeg is unavailable; missing
    # source media is intentionally replaced by a deterministic black clip.
    try:
        output = render_timeline(
            [ShortSegment("intro", "hello", 0.1, None)],
            str(tmp_path / "out.mp4"),
            width=64,
            height=64,
            fps=5,
        )
    except RuntimeError as exc:
        pytest.skip(str(exc))
    assert Path(output).is_file()
    assert Path(output).stat().st_size > 0
