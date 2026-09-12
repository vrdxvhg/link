# JARVIS V2 YouTube Automation - Build Status

## Connected foundation

- Local HTTP bridge with health, upload, list, download, authorization, and job APIs
- Persistent local job registry
- Background song-job worker
- Audio probing and scene planning
- Song project manifest generation
- End-to-end local pipeline runner
- FFmpeg-based MP4 renderer MVP with mood-adaptive visual treatment
- Thumbnail generation
- YouTube metadata generation
- Explicit human approval gate
- YouTube publish state machine
- Pluggable visual renderer interface
- YouTube Studio browser adapter contract with a safe dry-run implementation
- Voice activation/deactivation state machine, microphone adapter, RMS VAD, and runtime lifecycle
- Smoke tests and CI scaffolding

## Important boundary

The current renderer is an MVP and is not yet a true 3D/cinematic scene-generation system. The browser adapter is a contract plus dry-run implementation; a production YouTube Studio UI driver still needs to be attached and verified against the live Studio UI.

## Intended production path

`audio upload -> job -> probe -> scene plan -> visual renderer -> MP4 -> thumbnail -> metadata -> approval -> browser adapter -> YouTube Studio`

Public publishing must remain blocked until explicit approval is present.
