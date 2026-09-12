from scene_planner import build_scene_plan


def test_scene_plan_never_overshoots_duration():
    plan = build_scene_plan(10.0, bpm=120, mood="sad")
    scenes = plan["scenes"]
    assert scenes
    assert scenes[0]["start_seconds"] == 0.0
    assert scenes[-1]["end_seconds"] == 10.0
    assert all(scene["end_seconds"] > scene["start_seconds"] for scene in scenes)
    assert all(scene["end_seconds"] <= 10.0 for scene in scenes)


def test_scene_plan_preserves_beat_boundaries():
    plan = build_scene_plan(20.0, bpm=120, mood="punjabi")
    scenes = plan["scenes"]
    assert scenes[0]["end_seconds"] == 4.0
    assert scenes[1]["start_seconds"] == 4.0
    assert scenes[1]["end_seconds"] == 8.0
    assert scenes[-1]["end_seconds"] == 20.0
    assert all(scene["beat_sync"] for scene in scenes)


def test_unknown_mood_uses_cinematic_default():
    plan = build_scene_plan(5.0, bpm=100, mood="unknown")
    assert plan["scenes"][0]["visual_style"] == "cinematic_3d"
