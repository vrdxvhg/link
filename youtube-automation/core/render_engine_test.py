from __future__ import annotations

import unittest
from unittest.mock import patch

from render_engine import _color_for_mood, render_song_video


class RenderEngineTests(unittest.TestCase):
    def test_mood_palette_has_safe_fallback(self) -> None:
        self.assertEqual(_color_for_mood("romantic"), "0x3a1028")
        self.assertEqual(_color_for_mood("unknown"), "0x111827")

    @patch("render_engine.subprocess.run")
    @patch("render_engine.shutil.which", return_value="/usr/bin/ffmpeg")
    def test_render_builds_audio_video_command(self, _which, run) -> None:
        with patch("render_engine.Path.exists", return_value=True):
            result = render_song_video("song.wav", "out/final.mp4", width=1080, height=1920, fps=30, mood="punjabi")

        self.assertEqual(result, "out/final.mp4")
        command = run.call_args.args[0]
        self.assertIn("-shortest", command)
        self.assertIn("-i", command)
        self.assertIn("song.wav", command)
        self.assertIn("out/final.mp4", command)
        self.assertIn("s=1080x1920", " ".join(command))
        run.assert_called_once()


if __name__ == "__main__":
    unittest.main()
