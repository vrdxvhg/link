import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const root = path.dirname(new URL(import.meta.url).pathname);
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const js = fs.readFileSync(path.join(root, 'vrm_adapter.js'), 'utf8');
const css = fs.readFileSync(path.join(root, 'styles.css'), 'utf8');

assert.match(html, /id="vrm-canvas"/);
assert.match(html, /central VRM display/);
assert.match(js, /VRMUtils/);
assert.match(js, /GLTFLoader/);
assert.match(js, /head.*waist|HEAD.*WAIST/i);
assert.match(js, /mouth_open/);
assert.match(js, /jarvis-ui-state/);
assert.match(css, /center-slot/);

console.log('vrm shell static checks: OK');
