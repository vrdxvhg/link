import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.178.0/build/three.module.js';
import { OrbitControls } from 'https://cdn.jsdelivr.net/npm/three@0.178.0/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'https://cdn.jsdelivr.net/npm/three@0.178.0/examples/jsm/loaders/GLTFLoader.js';
import { VRMLoaderPlugin, VRMUtils } from 'https://cdn.jsdelivr.net/npm/@pixiv/three-vrm@3.4.2/lib/three-vrm.module.js';

const canvas = document.querySelector('#vrm-canvas');
const stateLabel = document.querySelector('#avatar-state');
const voiceMeter = document.querySelector('#voice-meter');
const runtimeStatus = document.querySelector('#runtime-status');
const vrmStatus = document.querySelector('#vrm-status');
const terminalLog = document.querySelector('#terminal-log');
const loading = document.querySelector('#loading');
const micStatus = document.querySelector('#mic-status');
const clock = document.querySelector('#clock');

const BRIDGE_URL = String(document.body.dataset.bridgeUrl || 'http://127.0.0.1:8787').replace(/\/$/, '');
const VRM_URL = String(document.body.dataset.vrmUrl || '../../assets/jarvis.vrm');
const STATE_POLL_MS = 500;

const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);
renderer.outputColorSpace = THREE.SRGBColorSpace;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(28, 1, 0.1, 100);
camera.position.set(0, 1.35, 3.2);

const hemi = new THREE.HemisphereLight(0x9efcff, 0x071018, 2.0);
scene.add(hemi);
const key = new THREE.DirectionalLight(0xffffff, 2.5);
key.position.set(1.5, 3, 2);
scene.add(key);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enablePan = false;
controls.enableZoom = false;
controls.target.set(0, 1.25, 0);
controls.update();

const grid = new THREE.GridHelper(4, 32, 0x1f6670, 0x103038);
grid.position.y = -0.62;
scene.add(grid);

let vrm = null;
let blinkClock = 0;
let currentState = {
  animation: 'idle',
  emotion: 'neutral',
  speaking: false,
  listening: false,
  locked: false,
  mouth_open: 0,
  voice_level: 0,
};

function log(line) {
  terminalLog.textContent += `\n${line}`;
  terminalLog.scrollTop = terminalLog.scrollHeight;
}

function resize() {
  const w = Math.max(1, canvas.clientWidth);
  const h = Math.max(1, canvas.clientHeight);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
  renderer.setSize(w, h, false);
}
window.addEventListener('resize', resize);
resize();

function setMorph(name, value) {
  if (!vrm?.expressionManager) return;
  const aliases = {
    mouth_open: ['aa'],
    blink: ['blink'],
    happy: ['happy'],
    sad: ['sad'],
    angry: ['angry'],
    surprised: ['surprised'],
  };
  for (const alias of aliases[name] || []) {
    try { vrm.expressionManager.setValue(alias, value); } catch (_) { /* model may not contain expression */ }
  }
}

function applyState(next) {
  currentState = { ...currentState, ...next };
  const readable = String(currentState.animation || 'idle').toUpperCase();
  stateLabel.textContent = readable;
  const level = Math.round(Math.max(0, Math.min(1, Number(currentState.voice_level || 0))) * 100);
  voiceMeter.textContent = `VOICE ${level}%`;
  runtimeStatus.textContent = currentState.listening ? '● LISTENING' : '○ INACTIVE';
  if (currentState.locked) runtimeStatus.textContent = '◈ LOCKED';
}

function animateVRM(dt, elapsed) {
  if (!vrm) return;
  if (vrm.update) vrm.update(dt);

  const speaking = Boolean(currentState.speaking);
  const idleBob = Math.sin(elapsed * 1.4) * 0.008;
  const talkBob = speaking ? Math.sin(elapsed * 6.0) * 0.012 : 0;
  vrm.scene.position.y = idleBob + talkBob;
  vrm.scene.rotation.y = Math.sin(elapsed * 0.35) * 0.025;

  if (currentState.animation === 'listen') {
    vrm.scene.rotation.x = Math.sin(elapsed * 1.8) * 0.018;
  } else if (currentState.animation === 'think') {
    vrm.scene.rotation.x = -0.035 + Math.sin(elapsed * 0.9) * 0.01;
  } else if (currentState.animation === 'alert') {
    vrm.scene.rotation.x = Math.sin(elapsed * 9.0) * 0.008;
  } else {
    vrm.scene.rotation.x = 0;
  }

  const mouth = speaking ? Math.max(0, Math.min(1, Number(currentState.mouth_open || 0))) : 0;
  setMorph('mouth_open', mouth);

  blinkClock += dt;
  const blink = blinkClock > 4.2 && blinkClock < 4.34 ? 1 : 0;
  if (blinkClock > 4.5) blinkClock = 0;
  setMorph('blink', blink);
  setMorph('happy', currentState.emotion === 'happy' ? 0.8 : 0);
  setMorph('sad', currentState.emotion === 'sad' ? 0.8 : 0);
  setMorph('angry', currentState.emotion === 'angry' ? 0.8 : 0);
  setMorph('surprised', currentState.emotion === 'surprised' ? 0.8 : 0);
}

async function loadVRM(url = VRM_URL) {
  loading.classList.remove('hidden');
  vrmStatus.textContent = 'LOADING';
  const loader = new GLTFLoader();
  loader.register((parser) => new VRMLoaderPlugin(parser));

  try {
    const gltf = await loader.loadAsync(url);
    vrm = gltf.userData.vrm;
    if (!vrm) throw new Error('Loaded model is not a valid VRM.');
    VRMUtils.removeUnnecessaryVertices(gltf.scene);
    VRMUtils.combineSkeletons(gltf.scene);
    vrm.scene.rotation.y = Math.PI;
    scene.add(vrm.scene);
    vrmStatus.textContent = 'READY';
    log(`VRM::LOADED ${url}`);
  } catch (error) {
    vrmStatus.textContent = 'NO MODEL';
    log(`VRM::WAITING ${error.message}`);
  } finally {
    loading.classList.add('hidden');
  }
}

function handleMessage(event) {
  if (!event.data || event.data.type !== 'jarvis-ui-state') return;
  const payload = event.data.payload || {};
  applyState(payload.vrm || payload);
  if (typeof payload.loading_visible === 'boolean') {
    loading.classList.toggle('hidden', !payload.loading_visible);
  }
}
window.addEventListener('message', handleMessage);

async function syncBridgeState() {
  try {
    const response = await fetch(`${BRIDGE_URL}/api/v1/ui/state`, { cache: 'no-store' });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const payload = await response.json();
    applyState(payload.vrm || {});
    loading.classList.toggle('hidden', !Boolean(payload.loading_visible));
    window.postMessage({ type: 'jarvis-ui-state', payload }, '*');
  } catch (error) {
    log(`BRIDGE::OFFLINE ${error.message}`);
  }
}
setInterval(syncBridgeState, STATE_POLL_MS);
syncBridgeState();

async function sendCommand(command) {
  const response = await fetch(`${BRIDGE_URL}/api/v1/ui/command`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ command }),
  });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || `HTTP ${response.status}`);
  applyState(payload.ui?.vrm || {});
  return payload;
}
window.JARVISCommand = sendCommand;

async function enableMicrophone() {
  if (!navigator.mediaDevices?.getUserMedia) return;
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const audio = new AudioContext();
    const source = audio.createMediaStreamSource(stream);
    const analyser = audio.createAnalyser();
    analyser.fftSize = 512;
    source.connect(analyser);
    const data = new Uint8Array(analyser.frequencyBinCount);
    micStatus.textContent = 'ON';
    function meter() {
      analyser.getByteTimeDomainData(data);
      let sum = 0;
      for (const value of data) { const n = (value - 128) / 128; sum += n * n; }
      const rms = Math.sqrt(sum / data.length);
      const level = Math.max(0, Math.min(1, rms * 4.5));
      if (currentState.speaking) applyState({ voice_level: level, mouth_open: Math.min(1, level * 1.35) });
      requestAnimationFrame(meter);
    }
    meter();
  } catch (error) {
    micStatus.textContent = 'DENIED';
    log(`MIC::${error.name}`);
  }
}

document.addEventListener('click', () => {
  if (micStatus.textContent === 'OFF') enableMicrophone();
}, { once: true });

const clockLoop = () => {
  clock.textContent = new Date().toLocaleTimeString();
  requestAnimationFrame(clockLoop);
};
clockLoop();

const rendererLoop = () => {
  requestAnimationFrame(rendererLoop);
  const now = performance.now() / 1000;
  const previous = rendererLoop.previous ?? now;
  const dt = Math.min(0.1, now - previous);
  rendererLoop.previous = now;
  animateVRM(dt, now);
  renderer.render(scene, camera);
};
rendererLoop();
loadVRM();
