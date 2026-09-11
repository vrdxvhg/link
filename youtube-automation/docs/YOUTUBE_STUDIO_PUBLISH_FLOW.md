# JARVIS V2 — YouTube Studio Publish Flow

## Target workflow

```text
Open YouTube Studio
  -> Create / Upload video
  -> Select final MP4
  -> Details
      -> AI title
      -> AI description
      -> custom thumbnail
      -> playlist
      -> audience
      -> altered/synthetic-content disclosure when applicable
  -> Checks
  -> Visibility
      -> Private / Unlisted / Schedule / Public
  -> Final approval
  -> Publish
```

## Browser automation requirements

The publisher should use a browser-control adapter rather than hard-coded screen coordinates. Prefer semantic selectors/accessibility roles and fall back to visual interaction only when necessary.

Required capabilities:

1. Launch/open YouTube Studio.
2. Confirm the intended Google/YouTube account/channel.
3. Start the upload workflow.
4. Select the rendered MP4 from the JARVIS job workspace.
5. Fill title and description.
6. Upload the generated custom thumbnail.
7. Configure playlist/audience and other configured metadata.
8. Handle upload/processing waits and transient UI changes.
9. Set visibility or schedule.
10. Stop at the final publish action until the job has an explicit approval token.
11. Click Publish/Save only after approval.
12. Capture the resulting video URL/ID and store it in the job record.

## Recovery

If the browser flow fails:

- keep the rendered MP4 and metadata in the job workspace;
- save the current publisher state;
- capture a diagnostic screenshot/log when available;
- allow the job to resume from the last completed stage;
- never regenerate the entire video unless the render itself is invalid.

## Policy-aware publishing

The generated content may be AI/synthetic. The publisher should expose the relevant YouTube disclosure/settings step instead of silently assuming a value. The user should be able to review this before publishing.

## Manual fallback

The system must always be able to export a complete upload package:

```text
final.mp4
thumbnail.png
title.txt
description.txt
tags.txt
publish.json
```

This lets the user finish the upload manually if browser automation is unavailable.
