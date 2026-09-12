import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { VRMUtils, VRMExpressionPresetName } from '@pixiv/three-vrm';

const canvas = document.querySelector('#vrm-canvas');
const statusNode = document.querySelector('#vrm-status');
const telemetry = document.querySelector('#telemetry');

const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);
renderer.outputColorSpace = THREE.SRGBColorSpace;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(22, 1, 0.1, 100);
camera.position.set(0, 1.45, 3.2);

scene.add(new THREE.HemisphereLight(0xbffcff, 0x081014, 2.2));
const key = new THREE.DirectionalLight(0x9cefff, 2.5);
key.position.set(1, 3, 2);
scene.add(key);

const avatarRoot = new THREE.Group();
scene.add(avatarRoot);
let currentVrm = null;
let targetMouth = 0;
let currentMouth = 0;
let animation = 'idle';

function resize() {
  const w = canvas.clientWidth || 1;
  const h = canvas.clientHeight || 1;
  renderer.setSize(w, h, false);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
}
window.addEventListener('resize', resize);

function applyExpression(name, weight) {
  if (!currentVrm?.expressionManager) return;
  currentVrm.expressionManager.setValue(name, weight);
}

function applyState(state = {}) {
  animation = state.animation || 'idle';
  targetMouth = Math.max(0, Math.min(1, Number(state.mouth_open || 0)));
  const emotion = state.emotion || 'neutral';
  const speaking = Boolean(state.speaking);

  if (currentVrm?.expressionManager) {
    currentVrm.expressionManager.setValue(VRMExpressionPresetName.Happy, emotion === 'happy' ? 0.7 : 0);
    currentVrm.expressionManager.setValue(VRMExpressionPresetName.Angry, emotion === 'angry' ? 0.5 : 0);
    currentVrm.expressionManager.setValue(VRMExpressionPresetName.Sad, emotion === 'sad' ? 0.55 : 0);
    currentVrm.expressionManager.setValue(VRMExpressionPresetName.Surprised, emotion === 'surprised' ? 0.45 : 0);
    currentVrm.expressionManager.setValue(VRMExpressionPresetName.Relaxed, emotion === 'relaxed' ? 0.55 : 0);
    if (!speaking) targetMouth = 0;
  }
}

window.JARVIS_VRM_STATE = applyState;

async function loadVrm(url) {
  statusNode.textContent = 'VRM LOADING…';
  const loader = new GLTFLoader();
  loader.crossOrigin = 'anonymous';
  const gltf = await loader.loadAsync(url);
  const vrm = gltf.userData.vrm;
  if (!vrm) throw new Error('Loaded asset is not a VRM model.');

  if (currentVrm) {
    avatarRoot.remove(currentVrm.scene);
    VRMUtils.deepDispose(currentVrm.scene);
  }
  VRMUtils.rotateVRM0(vrm);
  currentVrm = vrm;
  avatarRoot.add(vrm.scene);

  // Head-to-waist framing: keep only the upper body visible by camera framing.
  vrm.scene.position.y = -1.08;
  vrm.scene.position.z = 0;
  camera.lookAt(0, 1.15, 0);
  statusNode.textContent = 'VRM READY // HEAD → WAIST';
}

const modelUrl = window.JARVIS_VRM_URL || './assets/jarvis.vrm';
loadVrm(modelUrl).catch((error) => {
  console.warn(error);
  statusNode.textContent = 'VRM MODEL NOT ATTACHED';
});

function tick(timeMs) {
  const t = timeMs * 0.001;
  resize();
  currentMouth += (targetMouth - currentMouth) * 0.2;

  if (currentVrm) {
    const sway = Math.sin(t * (animation === 'speaking' ? 1.5 : 0.8)) * 0.012;
    currentVrm.scene.rotation.y = sway;
    currentVrm.scene.rotation.x = Math.sin(t * 0.7) * 0.004;
    applyExpression(VRMExpressionPresetName.Aa, currentMouth);
    currentVrm.update(1 / 60);
  }
  renderer.render(scene, camera);
  requestAnimationFrame(tick);
}
requestAnimationFrame(tick);

// Simple bridge hook for a desktop host/eDEX adapter.
window.addEventListener('jarvis-ui-state', (event) => {
  applyState(event.detail || {});
  telemetry.textContent = `SYSTEM// ONLINE\nVOICE// ${(event.detail?.voice_status || 'UNKNOWN').toUpperCase()}\nVRM// ${(event.detail?.central_module || 'VRM').toUpperCase()}\nFRAME// ${(event.detail?.central_framing || 'HEAD_TO_WAIST').toUpperCase()}`;
});
