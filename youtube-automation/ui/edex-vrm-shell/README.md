# JARVIS V2 — eDEX + 4D VRM shell

This folder is the desktop presentation surface for the locked eDEX-UI foundation.

## Visual lock

The surrounding eDEX shell is not redesigned. Loading behavior, panels, terminal/HUD language and technical composition remain intact.

The central terminal/workspace is the only replacement surface: a head-to-waist animated VRM character.

## Runtime behavior

The browser renderer consumes `jarvis-ui-state` `postMessage` payloads from the JARVIS UI runtime bridge. The VRM presentation supports idle, listening, speaking and thinking motion, simple emotion expressions, blinking and voice-level-driven mouth movement.

The canonical runtime remains in `youtube-automation/core`. Browser microphone RMS is only a local visual fallback; it is not the authoritative voice state.

## Model

Place the user's final VRM model at:

`youtube-automation/assets/jarvis.vrm`

The repository does not invent or fabricate the character asset.

## Local preview

From the repository root:

```text
python youtube-automation/ui/edex-vrm-shell/serve_ui.py --port 4173
```

Then open:

`http://127.0.0.1:4173/index.html`

Use an HTTP server rather than `file://` so ES modules and VRM assets load correctly.

## Integration path

`JarvisRuntime -> JARVISUIRuntime -> EDEXUIStateBridge -> postMessage -> edex_vrm_bridge.js -> vrm_app.js`

This keeps the UI renderer replaceable without coupling core job/voice logic to DOM selectors.
