from jobs import create_job, get_job, update_job


def test_job_lifecycle(tmp_path, monkeypatch):
    monkeypatch.setattr("jobs.JOBS_DIR", tmp_path)
    tmp_path.mkdir(exist_ok=True)
    job = create_job("song_to_youtube", {"file_id": "song.mp3"})
    assert job["status"] == "queued"
    assert get_job(job["id"])["kind"] == "song_to_youtube"
    updated = update_job(job["id"], status="running")
    assert updated["status"] == "running"
    assert get_job(job["id"])["status"] == "running"


if __name__ == "__main__":
    print("Run with pytest: python -m pytest test_jobs.py")
