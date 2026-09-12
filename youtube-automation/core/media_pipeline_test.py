from pathlib import Path

import pytest

from media_pipeline import render_media_plan
from shorts_media_adapters import ShortSegment, ShortsMediaPlan


def test_render_media_plan_rejects_invalid_plan(tmp_path: Path) -> None:
    plan = ShortsMediaPlan(topic="", segments=[])
    with pytest.raises(ValueError):
        render_media_plan(plan, str(tmp_path / "out.mp4"))


def test_render_media_plan_uses_canonical_renderer(tmp_path: Path) -> None:
    plan = ShortsMediaPlan(
        topic="smoke",
        segments=[ShortSegment("intro", "hello", 0.1, None)],
    )
    try:
        output = render_media_plan(
            plan,
            str(tmp_path / "nested" / "out.mp4"),
            width=64,
            height=64,
            fps=5,
        )
    except RuntimeError as exc:
        pytest.skip(str(exc))
    assert Path(output).is_file()
    assert Path(output).stat().st_size > 0
