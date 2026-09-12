from __future__ import annotations

try:
    from .edex_vrm_adapter import EDEXVRMAdapter
except ImportError:
    from edex_vrm_adapter import EDEXVRMAdapter


def check_payload_lock() -> None:
    adapter = EDEXVRMAdapter()
    payload = adapter.mount_payload({
        "shell": "edex",
        "voice_status": "speaking",
        "locked": False,
        "transition": "state_change",
        "vrm": {"animation": "speak", "mouth_open": 0.7, "voice_level": 0.5},
    })

    assert payload["shell"] == "edex"
    assert payload["central_module"] == "vrm"
    assert payload["central_framing"] == "head_to_waist"
    assert payload["vrm"]["framing"] == "head_to_waist"
    assert payload["vrm"]["renderer"] == "webgl-vrm"
    assert payload["vrm"]["lip_sync"] is True
    assert payload["vrm"]["animation"] is True
    assert payload["vrm"]["facial_expression"] is True


def check_manifest() -> None:
    manifest = EDEXVRMAdapter("assets/vrm/jarvis.vrm").model_manifest()
    assert manifest["format"] == "VRM"
    assert manifest["placement"] == "center_terminal_region"
    assert manifest["framing"] == "head_to_waist"


if __name__ == "__main__":
    check_payload_lock()
    check_manifest()
    print("edex_vrm_adapter: OK")
