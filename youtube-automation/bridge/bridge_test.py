"""Smoke tests for the JARVIS V2 bridge."""
from __future__ import annotations
import io
from app import app


def test_health():
    client = app.test_client()
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['ok'] is True


def test_upload_list_and_create_job(tmp_path, monkeypatch):
    import app as bridge
    import jobs
    monkeypatch.setattr(bridge, 'WORKSPACE', tmp_path)
    monkeypatch.setattr(jobs, 'JOBS_DIR', tmp_path / 'jobs')
    bridge.WORKSPACE.mkdir(parents=True, exist_ok=True)
    jobs.JOBS_DIR.mkdir(parents=True, exist_ok=True)
    client = app.test_client()
    response = client.post('/api/v1/files/upload', data={'file': (io.BytesIO(b'hello'), 'song.mp3')}, content_type='multipart/form-data')
    assert response.status_code == 201
    file_id = response.json['id']
    assert (tmp_path / file_id).exists()
    response = client.get('/api/v1/files')
    assert response.status_code == 200
    assert any(item['id'] == file_id for item in response.json['files'])
    response = client.post('/api/v1/jobs', json={'kind': 'song_to_youtube', 'payload': {'file_id': file_id}})
    assert response.status_code == 201
    assert response.json['status'] == 'queued'


if __name__ == '__main__':
    test_health()
    print('bridge smoke tests: PASS')
