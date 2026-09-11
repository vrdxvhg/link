# JARVIS V2 — Project Checkpoint

## Status

This checkpoint records the current JARVIS V2 / YouTube Automation architecture and implementation state so work can continue from here without losing the current decisions.

## Active project

**JARVIS V2 / YouTube Automation**

Do not switch this work to MYRA/V5 unless explicitly requested.

## Current architecture

Android App (paused) → YouTube Automation Bridge → workspace/uploads/jobs/metadata → JARVIS Core / Agents → media pipeline → YouTube Studio adapter

The backend/core must remain alive independently of the voice/UI listening layer.

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
- `youtube-automation/core/youtube_publish_flow.py`
- `youtube-automation/core/voice_control.py`
- `youtube-automation/core/voice_control_test.py`
- `youtube-automation/core/voice_control_test.py`
- `youtube-automation/core/speech_listener.py`
- `youtube-automation/core/runtime.py`
- `youtube-automation/core/runtime_test.py`
- `youtube-automation/core/__init__.py`
- `youtube-automation/core/README.md`
- `youtube-automation/core/VOICE_CONTROL.md`
- `youtube-automation/core/RUNTIME.md`
- `youtube-automation/core/requirements-voice.txt`

## Runtime work already added

The runtime layer connects the voice-control state machine with the listener/UI lifecycle. It is intended to provide:

- backend lifecycle independent from listener state
- listener start/stop handling
- runtime status reporting
- UI state callback integration
- command routing through `VoiceControl`
- demo/testable state transitions

## Important implementation note

The current speech listener supports recognized text and audio-file transcription, but live microphone capture must be treated as unfinished until the actual `sounddevice` capture loop is implemented and tested.

`sounddevice` is declared in `requirements-voice.txt` but is not by itself proof that live microphone capture is complete.

## Next execution order

1. Fix/package-safe imports in `speech_listener.py`.
2. Implement real live microphone capture with `sounddevice` + temporary WAV chunks + faster-whisper transcription.
3. Wire the capture loop into `runtime.py` without stopping the backend when listening is disabled.
4. Add runtime/microphone tests and a CLI demo.
5. Add the UI listening/locked status indicator.
6. Build the FFmpeg-based rendering MVP for the song factory.
7. Audit the uploaded source-library projects and extract only useful modules.
8. Implement the YouTube Studio adapter separately from the core state machine.
9. Keep final publishing behind the approval gate.

## Source library

The GitHub repository contains uploaded source-library ZIPs including BrowserUse, JARVIS, Jarvis-AI-Assistant, ai_desktop_agent, codex, computer-use-mcp, dax-assistant, edex-ui, libr-agent, munim-computer-use, windows-computer-use-mcp, FireRed-OpenStoryline and others. These are source material for audit/extraction, not evidence that their modules have already been integrated.

## Repository

`vrdxvhg/link`

Default branch: `main`

This file is a checkpoint only; it does not replace the actual source files or tests.
