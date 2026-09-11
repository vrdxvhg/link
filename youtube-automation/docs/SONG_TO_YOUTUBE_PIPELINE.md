# JARVIS V2 — AI Song to YouTube Pipeline

This is the first production workflow for the YouTube Automation project.

## User goal

The user provides an AI song/audio file. JARVIS should turn it into a polished music video, create metadata and thumbnail assets, and prepare the video for YouTube Studio publishing.

## Pipeline

```text
Song Library / Upload
        |
        v
[1] Audio Intake
        |
        +--> validate format/duration
        +--> extract BPM / waveform / loudness
        +--> identify language / mood / genre
        v
[2] Song Intelligence
        |
        +--> lyrics/transcript when available
        +--> chorus/verse/bridge timestamps
        +--> visual mood + story concept
        v
[3] Visual Director
        |
        +--> scene plan
        +--> 3D/cinematic visual style
        +--> beat-synced scene changes
        +--> camera movement / transitions
        v
[4] Video Factory
        |
        +--> generate/acquire visuals
        +--> animate stills where appropriate
        +--> sync visuals to audio
        +--> captions/lyrics when enabled
        +--> final render
        v
[5] Thumbnail + Metadata
        |
        +--> title candidates
        +--> description
        +--> hashtags/tags
        +--> custom thumbnail
        +--> playlist/category defaults
        v
[6] Review Gate
        |
        +--> render preview
        +--> metadata preview
        +--> thumbnail preview
        +--> user approval
        v
[7] YouTube Studio Publisher
        |
        +--> open YouTube Studio
        +--> Create / Upload video
        +--> select rendered video
        +--> set title/description/thumbnail
        +--> audience/settings
        +--> visibility
        +--> publish or schedule
        v
Published / Scheduled Video
```

## Important design decision

Publishing is behind an explicit review/approval gate. JARVIS can automate the repetitive upload workflow, but it should not silently publish a generated song/video without an explicit user-approved publish action.

## Music-video style engine

The default visual mode for the user's AI songs is **cinematic 3D-inspired music video**. The style director should derive the visual language from the song rather than applying one fixed template.

Inputs:

- genre
- language
- lyrical themes
- BPM/rhythm
- emotional arc
- song sections
- artist/channel branding

Possible visual treatments:

- cinematic 3D environments
- stylized 3D characters
- animated album-art worlds
- neon/cyber scenes
- rural/nature cinematic scenes
- romantic cinematic scenes
- devotional/spiritual cinematic scenes
- performance-stage scenes
- lyric-driven motion graphics

## Output assets

Each song job should produce a predictable workspace:

```text
jobs/<job_id>/
  source/
    song.ext
  analysis/
    song.json
    sections.json
    lyrics.json
  storyboard/
    scenes.json
  visuals/
    scene-001.*
    scene-002.*
  audio/
    normalized.*
  render/
    preview.mp4
    final.mp4
  metadata/
    title.json
    description.txt
    tags.json
  thumbnail/
    thumbnail.png
  publish/
    youtube-upload.json
```

## YouTube publisher states

```text
DRAFT
  -> READY_FOR_REVIEW
  -> APPROVED
  -> UPLOADING
  -> PROCESSING
  -> SCHEDULED | PUBLISHED
  -> FAILED
```

## Safety / reliability

- Never store YouTube credentials in Git.
- Keep secrets in environment/configuration storage.
- Validate generated media before upload.
- Preserve the original audio file.
- Keep intermediate renders so failed jobs can resume.
- Make publish a deliberate, auditable action.
- Record the final YouTube URL/video ID after successful publication when available.
