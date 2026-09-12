# JARVIS V2 — 4D VRM Renderer Contract

## Visual lock

The desktop shell remains the selected eDEX-UI foundation. The renderer must not redesign the surrounding shell, loading screens, transitions, panels, terminal/HUD language, or technical composition.

Only the central workspace is replaced with the JARVIS avatar presentation.

## Central avatar framing

- Model: VRM / 4D animated character
- Visible crop: head through waist only
- No legs or lower-body presentation
- Centered inside the existing main workspace
- The avatar is a visual module, not a replacement for the surrounding eDEX panels

## Real-time animation inputs

The renderer consumes the JSON snapshot exposed by `VRMController` / `EDEXUIStateBridge`.

### Core states

- `idle` — neutral idle loop
- `listen` — attentive/listening animation
- `think` — thinking animation
- `speak` — speaking animation with lip sync
- `alert` — error/attention animation

### Expression

Emotion is independent from the runtime animation so the renderer can blend facial expressions without changing the shell or command state.

## Voice / lip sync

`voice_level` is normalized to `0.0..1.0`.

When `speaking=true`, `mouth_open` is derived from the voice level and is clamped to `0.0..1.0`. A production renderer should use this as the minimum mouth-animation driver and may replace it with phoneme/viseme timing when the speech engine exposes it.

When speech ends, the mouth pose must return to neutral.

## UI audio/visual synchronization

The same runtime event should drive:

1. voice waveform/level indicator in the eDEX shell,
2. VRM speaking/listening state,
3. mouth/lip animation,
4. emotion/gesture state.

The core runtime must not depend on DOM, canvas, WebGL, or a specific VRM engine.

## Future renderer adapters

Allowed implementations include Three.js/WebGL, Electron/WebView, native desktop WebGL, or another VRM-capable renderer. All implementations must consume the same render-neutral state contract.

## Acceptance checks

- eDEX shell remains visually intact.
- Central workspace contains only head-to-waist VRM presentation.
- Listening and speaking states visibly change the avatar animation.
- Speech level drives mouth movement while speaking.
- Lock/inactive states reach the UI without stopping JARVIS Core.
- Loading/transition state remains controlled by the eDEX UI layer.
