# Alphatalks3000 3D Renderer (Remotion + Three.js) — free via GitHub Actions

## Setup (one time, free)
1. Create a GitHub account (free) and a new **public** repo, e.g. `alphatalks-3d`.
   Public repos get unlimited free Actions minutes. Private repos get 2,000 free minutes per month.
2. Upload all files from this folder to the repo (keep the `.github/workflows/render.yml` path).
3. In GitHub: Settings > Developer settings > Personal access tokens > Fine-grained token.
   Repository access: only this repo. Permissions: Actions = Read and write, Contents = Read and write.
4. In n8n, create a credential with this token (done through the n8n setup card).

## How a render works
- n8n calls `POST https://api.github.com/repos/<owner>/<repo>/actions/workflows/render.yml/dispatches`
  with body `{ "ref": "main", "inputs": { "job_id": "job-123", "composition": "Story3D", "props": "<JSON string>" } }`.
- GitHub renders the video (about 5–20 minutes for a few minutes of video).
- The video appears as a release asset: `GET https://api.github.com/repos/<owner>/<repo>/releases/tags/job-123`
  -> `assets[0].browser_download_url`.

## Props format
{ "title": "...", "musicUrl": "https://...mp3", "musicVolume": 0.15,
  "scenes": [ { "type": "sunrise|workout|shield|orbit|path", "durationSec": 6,
                "chapterTitle": "Chapter 1 — ...", "caption": "narration text",
                "voiceoverUrl": "https://...mp3", "color": "#f5b942" } ] }

## Local preview (optional)
npm install && npm run studio
