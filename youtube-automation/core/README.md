# JARVIS V2 Core

The first executable foundation for the song-to-YouTube pipeline.

## Current modules

- `song_factory.py` — turns a local song into a structured project manifest and output workspace.
- `youtube_publish_flow.py` — validates the finished video/thumbnail/metadata package and enforces an approval gate before publishing.

## Intended pipeline

```text
Song file
  -> media probe
  -> song project manifest
  -> lyrics / beat / mood analysis
  -> cinematic 3D scene plan
  -> render
  -> thumbnail + YouTube metadata
  -> YouTube Studio upload
  -> human approval
  -> publish / schedule
```

FFmpeg is the planned media foundation because it supports transcoding and simple/complex audio-video filter graphs. The actual 3D renderer is kept modular so it can be selected from the audited V1 tools instead of hard-coding one renderer.
