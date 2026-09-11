# JARVIS V2 Runtime

`runtime.py` is the integration point between speech recognition, voice commands, and the UI state.

```text
Microphone / audio
      ↓
SpeechListener / ASR
      ↓
VoiceControl
      ↓
JarvisRuntime
      ├── UI state callback
      └── backend remains running
```

## Required behavior

- `I am Vikas` toggles listening/UI interaction.
- `Deactivate system` disables listening/UI interaction.
- `Activate system` and `Continue listening` enable it.
- `Lock` blocks ordinary activate/deactivate commands.
- `Unlock` removes that block.
- `I am Vikas` remains the explicit wake/toggle phrase while locked.
- Deactivation does **not** terminate the backend.

## Programmatic entry points

- `JarvisRuntime.command(text)` — route recognized speech text.
- `JarvisRuntime.audio_file(path)` — transcribe a recorded clip using the optional ASR adapter.
- `JarvisRuntime.status()` — obtain backend/listening/lock state for the UI.
