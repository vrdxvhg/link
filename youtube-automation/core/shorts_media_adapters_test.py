from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from shorts_media_adapters import ShortSegment, ShortsMediaPlan, build_short_plan, render_with_provider


class ShortsMediaAdaptersTests(unittest.TestCase):
    def test_build_plan_preserves_order_and_metadata(self) -> None:
        plan = build_short_plan(
            "test topic",
            {
                "title": "Test title",
                "description": "Test description",
                "tags": ["a", "b"],
                "intro": "Opening line",
                "points": [
                    {"heading": "First", "body": "Point body"},
                    {"heading": "Second", "body": "Another body"},
                ],
                "outro": "Closing line",
            },
        )

        self.assertEqual(
            [segment.label for segment in plan.segments],
            ["intro", "point_1", "point_2", "outro"],
        )
        self.assertEqual(plan.title, "Test title")
        self.assertEqual(plan.tags, ["a", "b"])
        self.assertGreater(plan.duration_seconds, 0)

    def test_footage_provider_is_called_for_each_segment(self) -> None:
        queries: list[str] = []

        class Provider:
            def search(self, query: str, *, vertical: bool = True) -> str | None:
                queries.append(query)
                self_vertical = vertical
                return f"/media/{len(queries)}.mp4" if self_vertical else None

        plan = build_short_plan(
            "topic",
            {"intro": "Hello", "points": [{"heading": "One", "body": "World"}]},
            footage_provider=Provider(),
        )

        self.assertEqual(len(queries), 2)
        self.assertEqual(plan.segments[0].media_path, "/media/1.mp4")
        self.assertEqual(plan.segments[1].media_path, "/media/2.mp4")

    def test_render_adapter_creates_parent_directory(self) -> None:
        plan = ShortsMediaPlan(
            topic="topic",
            segments=[ShortSegment("intro", "hello", 1.0)],
        )

        calls: list[tuple[list[ShortSegment], str]] = []

        def renderer(segments, output_path: str) -> str:
            calls.append((list(segments), output_path))
            Path(output_path).write_text("rendered", encoding="utf-8")
            return output_path

        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "nested" / "result.mp4"
            result = render_with_provider(plan, renderer, str(output))
            self.assertEqual(result, str(output))
            self.assertTrue(output.exists())
            self.assertEqual(calls[0][0][0].label, "intro")

    def test_validation_rejects_empty_or_invalid_plans(self) -> None:
        with self.assertRaises(ValueError):
            ShortsMediaPlan(topic="", segments=[ShortSegment("x", "y", 1)]).validate()
        with self.assertRaises(ValueError):
            ShortsMediaPlan(topic="topic", segments=[]).validate()
        with self.assertRaises(ValueError):
            ShortsMediaPlan(topic="topic", segments=[ShortSegment("x", "y", 0)]).validate()


if __name__ == "__main__":
    unittest.main()
