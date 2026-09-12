# JARVIS V2 — Central 4D VRM Shell Adapter

This is the desktop presentation prototype for the **locked eDEX-UI shell**.

## Rule

The surrounding eDEX composition is not redesigned. The adapter only owns the central visual slot where the old terminal/main-display content is replaced by a head-to-waist VRM avatar.

## Features

- head-to-waist framing
- VRM load target from `window.JARVIS_VRM_URL`
- idle/listening/speaking/thinking/alert animation state mapping
- expression/emotion hooks
- voice-level driven mouth/lip-sync control
- transparent central canvas so the surrounding eDEX HUD remains visible
- JSON state input compatible with `core/ui_state_bridge.py`

## Prototype run

Open `index.html` from a local HTTP server. The page uses browser ESM imports so the prototype can be evaluated without modifying JARVIS Core.

The actual `edex-ui-master.zip` source remains the visual source-of-truth; this folder is an isolated VRM integration surface until the eDEX source archive is unpacked into the desktop application.

## Expected model

Set `window.JARVIS_VRM_URL` to a local `.vrm` asset. No VRM binary is committed to the repository by this adapter.
