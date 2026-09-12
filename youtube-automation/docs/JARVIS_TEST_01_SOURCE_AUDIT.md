# JARVIS_TEST_01 — OneDrive Source Audit

Source folder: `Desktop/JARVIS_TEST_01` in the connected OneDrive.

## Files discovered

- `.venv/` — local environment; **do not import**.
- `jarvis-main/` — JARVIS source; audit separately and extract reusable architecture only.
- `JARVIS_V1_Working.zip` — prior JARVIS implementation; source material, not a drop-in replacement.
- `libr-agent-main.zip` — agent/tooling source; candidate for task orchestration and tool routing.
- `moviepy-master.zip` — video editing/media composition library; candidate for higher-level editing helpers.
- `munim-computer-use-main.zip` — computer-use source; candidate for controlled desktop automation.
- `remotion-main.zip` — programmatic video/rendering source; strong candidate for timeline/scene composition.
- `youtube_tool-master.zip` — YouTube automation source; candidate modules include script generation, stock clip acquisition, video generation, voice generation, metadata and YouTube profile management.
- `yt-automation-main.zip` — compact end-to-end Shorts pipeline; useful patterns for script → TTS → stock footage → visual composition → FFmpeg → YouTube upload.
- `pdf.svg`, `powerpoint_20x1.svg` — UI/assets only; not core runtime modules.

## Extraction policy

The JARVIS V2 repository remains the canonical implementation. These files are **source material**. Do not blindly merge complete projects or duplicate runtimes.

### Highest-priority extraction

1. **Video editing/rendering**
   - Remotion concepts for deterministic scene/timeline composition.
   - MoviePy utilities where they provide functionality not already covered by the FFmpeg renderer.
   - `yt-automation` visual builder and video assembler patterns.
   - `youtube_tool/GenerateVideo` and `GenerateVoice` patterns.

2. **YouTube automation**
   - `yt-automation` script/voice/footage/metadata/upload separation.
   - `youtube_tool/YoutubeBot` and profile-management patterns.
   - Keep JARVIS approval gate as the controlling publish boundary.

3. **Agent/computer-use**
   - `libr-agent` and `munim-computer-use` are candidates for controlled tool execution and desktop automation.
   - Integrate through adapters/interfaces rather than replacing JARVIS Core.

4. **Security / hacking-related material**
   - Only defensive, sandboxed, auditing and system-hardening capabilities should be integrated into JARVIS V2.
   - Offensive intrusion, credential theft, persistence, malware, destructive automation or unauthorized-access functionality must not be wired into the project.

## Current JARVIS V2 integration direction

`audio/song -> analysis -> scene plan -> visual renderer -> MP4 -> thumbnail -> metadata -> human approval -> YouTube adapter`

The newly discovered Shorts sources should extend this pipeline as optional capabilities, not replace the existing song pipeline.

## Next extraction batches

- Batch A: Shorts/video composition adapter.
- Batch B: stock-footage and media-source adapter.
- Batch C: TTS/voice adapter.
- Batch D: YouTube upload/profile adapter review.
- Batch E: agent/computer-use adapter review.

No secrets, `.venv` contents, cached bytecode, tokens or local credentials should be copied into GitHub.
