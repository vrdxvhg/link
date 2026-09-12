# JARVIS V2 — eDEX + 4D VRM shell prototype

This folder is the desktop renderer surface for the locked eDEX-UI foundation.

## Locked visual rule

The surrounding eDEX-style shell is preserved. The center terminal/workspace is the only intended visual replacement: it hosts a head-to-waist VRM avatar. Loading, panels, HUD/technical composition and runtime status remain part of the shell.

## Renderer

`vrm_app.js` uses Three.js + `@pixiv/three-vrm` and expects the model at:

`youtube-automation/assets/jarvis.vrm`

The model is intentionally an external asset and is not fabricated by this prototype.

## Runtime state

The renderer accepts `postMessage` events shaped as:

```js
window.postMessage({
  type: "jarvis-ui-state",
  payload: {
    loading_visible: false,
    vrm: {
      animation: "speak",
      emotion: "confident",
      speaking: true,
      listening: false,
      mouth_open: 0.72,
      voice_level: 0.55
    }
  }
});
```

The microphone meter uses Web Audio RMS as a local fallback. The canonical JARVIS runtime remains the source of truth; this browser-side meter is only a presentation aid.

## Local preview

Serve the repository from a local HTTP server so ES modules and `.vrm` assets load correctly. Do not open `index.html` directly from `file://`.
