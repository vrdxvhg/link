from voice_control import ListenerState, VoiceControl


def check():
    v = VoiceControl()
    assert v.handle("I am Vikas") is ListenerState.INACTIVE
    assert v.handle("I am Vikas") is ListenerState.LISTENING
    assert v.handle("deactivate system") is ListenerState.INACTIVE
    assert v.handle("continue listening") is ListenerState.LISTENING
    v.handle("lock")
    assert v.locked is True
    assert v.handle("deactivate system") is ListenerState.LISTENING
    v.handle("I am Vikas")
    assert v.state is ListenerState.INACTIVE
    v.handle("unlock")
    assert v.locked is False
    assert v.handle("activate system") is ListenerState.LISTENING


if __name__ == "__main__":
    check()
    print("voice_control: OK")
