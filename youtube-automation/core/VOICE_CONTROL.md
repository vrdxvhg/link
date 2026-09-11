# JARVIS V2 Voice Control

The voice-control layer is independent from the backend. Deactivating listening does not terminate JARVIS services.

| Voice phrase | Action |
|---|---|
| `I am Vikas` | Toggle listening/UI interaction off or back on |
| `Continue listening` | Activate listening |
| `Activate system` | Activate listening |
| `Deactivate system` | Deactivate listening/UI interaction |
| `Lock` | Lock ordinary activation/deactivation commands |
| `Unlock` | Unlock ordinary activation/deactivation commands |

`I am Vikas` remains the explicit toggle while locked so the user can wake the interface again.

## Current implementation

`core/voice_control.py` contains a small state machine with two listener states:

- `listening`
- `inactive`

The microphone/speech-recognition provider and the graphical UI should call `VoiceControl.handle()` after speech recognition. The provider is intentionally not hard-coded here, so Whisper, Windows Speech, browser speech recognition, or another recognizer can be plugged in later.
