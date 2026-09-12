/**
 * JARVIS V2 browser bridge for the locked eDEX shell.
 *
 * Keeps JARVIS runtime events separate from the visual shell. The central
 * terminal slot is treated as a host; the surrounding eDEX DOM is untouched.
 */

const STATE_EVENT = 'jarvis-ui-state';

export function createEDEXVRMBridge({ root = document } = {}) {
  const canvas = root.querySelector('#vrm-canvas');
  const central = root.querySelector('#central-terminal');
  const runtime = root.querySelector('#runtime-status');
  const loading = root.querySelector('#loading');

  if (!canvas || !central) {
    throw new Error('JARVIS VRM host elements are missing from the eDEX shell.');
  }

  const state = {
    shell: 'edex',
    central_module: 'vrm',
    central_framing: 'head_to_waist',
    loading_visible: false,
    voice_status: 'listening',
    locked: false,
    vrm: {},
  };

  function apply(payload = {}) {
    Object.assign(state, payload);
    if (payload.vrm) state.vrm = { ...state.vrm, ...payload.vrm };
    central.dataset.centralModule = state.central_module;
    central.dataset.framing = state.central_framing;
    central.dataset.animation = state.vrm.animation || 'idle';
    central.dataset.emotion = state.vrm.emotion || 'neutral';
    central.dataset.speaking = String(Boolean(state.vrm.speaking));
    central.dataset.listening = String(Boolean(state.vrm.listening));

    if (runtime) {
      runtime.textContent = state.locked
        ? '◈ LOCKED'
        : state.voice_status === 'listening'
          ? '● LISTENING'
          : '○ INACTIVE';
    }

    if (loading) loading.classList.toggle('hidden', !Boolean(state.loading_visible));
    canvas.dispatchEvent(new CustomEvent(STATE_EVENT, { detail: { ...state } }));
    return { ...state, vrm: { ...state.vrm } };
  }

  function onMessage(event) {
    if (event.data?.type !== STATE_EVENT) return;
    apply(event.data.payload || {});
  }

  window.addEventListener('message', onMessage);
  apply();

  return {
    apply,
    snapshot: () => ({ ...state, vrm: { ...state.vrm } }),
    destroy: () => window.removeEventListener('message', onMessage),
  };
}
