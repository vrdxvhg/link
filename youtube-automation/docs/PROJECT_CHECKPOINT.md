# JARVIS V2 — Project Checkpoint

## Status

This checkpoint records the current JARVIS V2 / YouTube Automation architecture and implementation state so work can continue from here without losing the current decisions.

## Active project

**JARVIS V2 / YouTube Automation**

Do not switch this work to MYRA/V5 unless explicitly requested.

## Current architecture

Android App (paused) → YouTube Automation Bridge → workspace/uploads/jobs/metadata → JARVIS Core / Agents → media pipeline → YouTube Studio adapter

The backend/core remains alive independently from the voice/UI listening layer.

## Song-to-YouTube pipeline

Song file → media/audio analysis → lyrics/sections → mood/genre → cinematic 3D storyboard → beat/lyrics synchronization → render final MP4 → thumbnail → title/description/SEO metadata → review/approval → YouTube Studio upload → publish/schedule.

Visual direction is adaptive to the song: romantic, Punjabi/desi, sad, devotional, energetic, rural/farming, etc.

A human approval gate is mandatory before public publishing.

## Voice control — locked behavior

- `Continue listening` → listening ON
- `Activate system` → listening ON
- `Deactivate system` → listening OFF / UI interaction inactive
- `I am Vikas` → toggle listening/UI state
  - ON → OFF
  - OFF → ON
- `Lock` → blocks ordinary activation/deactivation commands
- `Unlock` → restores ordinary activation/deactivation commands
- `I am Vikas` remains an explicit wake/toggle command while locked.

Shutdown/deactivation affects only the voice-listening/UI interaction layer. It must NOT kill the JARVIS backend.

`I am Vikas` is a command trigger, not an identity/authentication mechanism.

## Implemented core files

- `youtube-automation/core/song_factory.py`
- `youtube-automation/core/pipeline_runner.py`
- `youtube-automation/core/render_engine.py`
- `youtube-automation/core/youtube_publish_flow.py`
- `youtube-automation/core/voice_control.py`
- `youtube-automation/core/voice_control_test.py`
- `youtube-automation/core/speech_listener.py`
- `youtube-automation/core/speech_listener_test.py`
- `youtube-automation/core/runtime.py`
- `youtube-automation/core/runtime_test.py`
- `youtube-automation/core/runtime_cli.py`
- `youtube-automation/core/jarvis_runtime.py` (compatibility shim to canonical runtime)
- `youtube-automation/core/microphone_listener.py`
- `youtube-automation/core/voice_vad.py`
- `youtube-automation/core/approval_gate.py`
- `youtube-automation/core/youtube_adapter.py`
- `youtube-automation/core/youtube_browser_adapter.py`
- `youtube-automation/core/vrm_controller.py`
- `youtube-automation/core/vrm_controller_test.py`
- `youtube-automation/core/__init__.py`
- `youtube-automation/core/README.md`
- `youtube-automation/core/VOICE_CONTROL.md`
- `youtube-automation/core/RUNTIME.md`
- `youtube-automation/core/requirements-voice.txt`

## Runtime / microphone status

Live microphone capture is implemented in `speech_listener.py` using lazy `sounddevice` capture, temporary WAV chunks, and local `faster-whisper` transcription. `runtime.py` owns the microphone thread and keeps the backend alive when listening is disabled.

Hardware-free tests cover the runtime state machine, microphone thread lifecycle, and one captured/transcribed microphone chunk. `runtime_cli.py` provides a command-line smoke/demo entry point. The legacy `jarvis_runtime.py` entry point now delegates to `runtime.py` so there is one canonical runtime implementation.

The microphone stack remains optional: the core runtime can start without `sounddevice`/`faster-whisper`; live capture reports a dependency error only when explicitly started.

## Bridge / media pipeline status

The local Bridge exposes health, authenticated file upload/list/download, asynchronous job creation/status, and approval-gated song jobs. The pipeline runner already connects song project creation → FFmpeg render → metadata → thumbnail → `awaiting_approval` manifest state.

The current FFmpeg renderer is an MVP adapter: it produces a 1920×1080 H.264/AAC video with a mood-dependent cinematic background, subtle zoom and vignette. It is intentionally a replaceable rendering layer for the future 3D/VRM scene renderer.

The YouTube Studio layer already has a core publish state machine plus browser-adapter contract/dry-run implementation. A production browser driver still needs live Studio verification.

## 4D VRM UI milestone

The eDEX-UI shell remains locked. The central terminal/main display region is reserved for the animated **head-to-waist 4D VRM avatar**; the surrounding panels, loading screens, transitions, effects, terminal/HUD language and overall composition are not to be redesigned.

`youtube-automation/core/vrm_controller.py` now provides a render-neutral adapter boundary with:

- head-to-waist framing
- listening / speaking / idle / thinking / alert animation states
- emotion state
- live voice level
- mouth-open intensity for lip-sync
- locked/listening state

`vrm_controller_test.py` covers runtime mapping, voice-level normalization, speaking transitions and lip-sync mouth reset. The final desktop renderer still needs to connect these states to the actual eDEX visual layer and production VRM runtime.

## Remaining execution order

1. Verify the latest CI run and fix any environment/import failures.
2. Harden Bridge API/job tests and approval-state transitions.
3. Connect runtime voice/listening state to the new VRM controller and locked eDEX UI shell.
4. Replace/extend the FFmpeg MVP with the real song-driven 3D/VRM scene pipeline.
5. Audit the uploaded source-library projects and extract only useful modules.
6. Verify/attach the production YouTube Studio browser driver against the live Studio UI.
7. Keep final publishing behind the approval gate.

## UI lock

`youtube-automation/docs/JARVIS_V2_UI_LOCK.md` is the visual source-of-truth constraint. Preserve the selected eDEX-UI shell, loading screens, transitions, effects, panels, terminal/HUD language and overall composition. The intended central visual replacement is the head-to-waist animated VRM/3D character; do not redesign the surrounding shell.

## Source library

The GitHub repository contains uploaded source-library ZIPs including BrowserUse, JARVIS, Jarvis-AI-Assistant, ai_desktop_agent, codex, computer-use-mcp, dax-assistant, edex-ui, libr-agent, munim-computer-use, windows-computer-use-mcp, FireRed-OpenStoryline and others. These are source material for audit/extraction, not evidence that their modules have already been integrated.

## Repository

`vrdxvhg/link`

Default branch: `main`

This file is a checkpoint only; it does not replace the actual source files or tests.
