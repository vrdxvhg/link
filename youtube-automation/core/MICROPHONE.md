# JARVIS V2 — Live Microphone Layer

The voice stack now has three layers:

`MicrophoneListener → SpeechListener/faster-whisper → VoiceControl → Runtime/UI`

## Behavior

- `Activate system` / `Continue listening` keeps listening active.
- `Deactivate system` makes the listener inactive.
- `I am Vikas` toggles listening/UI interaction on or off.
- `Lock` blocks ordinary activation/deactivation commands.
- `Unlock` restores ordinary commands.
- Lock does not block `I am Vikas`.

## Important

This is an optional local microphone adapter. It requires `sounddevice`, `numpy`, and `faster-whisper`. The backend remains separate from the listener, so deactivating listening does not terminate JARVIS.

## Run from the core directory

```bash
python -m youtube_automation.core.microphone_listener
```

The adapter is intentionally small so a future Windows audio/VAD adapter can replace it without changing the command state machine.
