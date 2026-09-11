# JARVIS V2 Bridge — local run

```bash
python -m pip install -r youtube-automation/bridge/requirements.txt
python -m youtube_automation.bridge.app
```

Default endpoint: `http://127.0.0.1:8787`

Health: `GET /health`

Upload: `POST /api/v1/files/upload` with multipart field `file`

Create song job: `POST /api/v1/jobs`

```json
{"kind":"song_to_youtube","payload":{"file_id":"song.mp3","bpm":120,"mood":"cinematic"}}
```

Job status: `GET /api/v1/jobs/<id>`

The worker currently builds the project manifest asynchronously. Rendering and final YouTube publishing remain separate stages, with publishing gated by explicit approval.
