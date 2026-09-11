# YouTube Automation — Phone Bridge

A dedicated project for the YouTube Automation system.

## Goal

Phone → Bridge API → Workspace → YouTube Automation project.

The first milestone is a reliable file gateway so files uploaded from the phone can be received by the backend, stored in a controlled workspace, inspected by automation tools, and later integrated into the project.

## Architecture

```text
Android App (Phone)
        |
        | HTTPS / LAN
        v
YouTube Automation Bridge
        |
        +--> uploads/
        +--> workspace/
        +--> jobs/
        +--> metadata/
        |
        v
Automation Core / Agents
```

## Initial API

- `GET /health` — bridge health/status
- `POST /api/v1/files/upload` — multipart file upload
- `GET /api/v1/files` — list uploaded files
- `GET /api/v1/files/{id}` — file metadata
- `GET /api/v1/files/{id}/download` — download a stored file

## Security principles

- Never expose arbitrary filesystem paths through the API.
- Keep uploaded files inside the configured workspace.
- Validate filenames and file sizes.
- Use an access token before exposing the bridge outside localhost/LAN.
- Keep secrets out of Git.

## Project status

Foundation created. Android APK/client and full automation integration will be added after the Bridge API is tested independently.
