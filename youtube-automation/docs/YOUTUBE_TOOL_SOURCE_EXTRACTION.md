# JARVIS V2 — YouTube Tool Source Extraction

Source: `youtube_tool-master.zip` from `JARVIS_TEST_01`.

## Decision

Do not copy this project wholesale into JARVIS V2. Extract reusable behavior behind JARVIS-native interfaces and keep the original archive as source material.

## Useful capabilities identified

### 1. Video assembly
`GenerateVideo/main.py` contains a manual video generator that:
- combines downloaded clips,
- concatenates clips with FFmpeg,
- attaches generated audio,
- can produce subtitle output,
- supports a configurable average clip duration.

**JARVIS action:** reuse the pipeline concepts in the existing renderer instead of importing the original generator and its path/database assumptions.

### 2. Audio-duration driven timing
`GenerateVideo/utils/audio.py` uses FFprobe to obtain media duration. The source also calculates an approximate number of visual clips from audio duration.

**JARVIS action:** timing belongs in the media-plan/render stage. Exact segment timing should come from the generated audio whenever available; word-count timing remains only a fallback.

### 3. Voice providers
`GenerateVoice/main.py` contains ElevenLabs and local/manual voice paths.

**JARVIS action:** keep voice generation behind the existing provider abstraction. API keys must come from runtime configuration/environment and never be copied from source archives.

### 4. Stock footage
The source has Pexels and Mixkit collectors with portrait/vertical search behavior.

**JARVIS action:** expose stock search/download through a footage-provider adapter. Do not import scraper caches, credentials, browser state, or generated downloads.

### 5. YouTube publishing
`YoutubeBot/main.py` contains browser-based YouTube Studio publishing behavior.

**JARVIS action:** keep the existing JARVIS YouTube Studio adapter and mandatory approval gate as the canonical publishing path. Source browser automation is reference material only.

### 6. Metadata
`API/utils/video_metadata.py` contains an FFmpeg-based metadata/transcoding helper.

**JARVIS action:** consolidate equivalent encoding/metadata behavior into the existing JARVIS media renderer/metadata generator instead of maintaining a second utility stack.

## Explicitly excluded from integration

- `__pycache__` and compiled bytecode
- bundled/generated media such as `received_video.mp4`
- bundled FFmpeg binaries and documentation (JARVIS should use a configured system/runtime FFmpeg)
- source logs
- local database credentials/configuration
- API keys/tokens/secrets
- source-specific PostgreSQL database coupling
- source-specific hard-coded Windows paths
- scraper/browser state

## Security boundary

JARVIS V2 may use automation for the user's own authorized YouTube workspace and defensive system operations. No offensive intrusion, credential theft, persistence, malware, destructive automation, or unauthorized access is extracted from source libraries.

## Current integration point

`core/shorts_media_adapters.py` provides the JARVIS-native intermediate media-plan contracts. Tests are in `core/shorts_media_adapters_test.py`.

## Next extraction targets

1. Improve audio-duration/timeline integration in the canonical JARVIS renderer.
2. Add concrete Pexels/Mixkit provider adapters with explicit configuration and safe download handling.
3. Add provider tests using mocks; no network or credentials in unit tests.
4. Consolidate YouTube metadata/transcoding behavior without duplicating the existing JARVIS pipeline.
