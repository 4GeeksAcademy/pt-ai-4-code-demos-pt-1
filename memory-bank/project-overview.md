# Tag Maker Project — Repository Memory

## Project Purpose
A web app for creating tag/badge-style images (like Discord tags or presentation labels) with a Vue 3 frontend and Python backend deployed on Vercel.

## Architecture
- **Frontend**: Vue 3 + Vite + Pinia + Tailwind CSS + PrimeVue SPA
- **Backend**: Python serverless function on Vercel using `http.server.BaseHTTPRequestHandler`
- **Image Generation**: Pillow (PIL) compositing of PNG assets with custom text and colors
- **Live API**: `https://discord-tagger.vercel.app/?q=[{"text":"...","bg":"#hex","color":"#hex"},...]`

## Backend (`/backend`)
- `app.py` — Active/deployed Vercel handler. Uses `PIL` to composite tags from `cap.png` and `body.png` image assets. Accepts GET with `?q=` JSON param.
- `backend/images/tag.py` — Older/duplicate version of the tag generation logic with `COLORS` enum.
- `oops.py` — Utility script for RGBA→hex conversion.
- Assets: `cap.png`, `body.png`, `label.png`, `label.svg`, `NowAlt-Regular.otf` font.
- Deployed via Vercel using `@vercel/python`.

## Frontend (`/frontend`)
- **HomeView.vue** — Main page with live tag preview + editor list.
- **TagEditor.vue** — Per-tag editor with text input, bg/text color pickers, copy/delete.
- **stores/tags.js** — Pinia store managing tags array and generating debounced API URL.
- **router/index.js** — Single route `/`.
- Dependencies: Vue 3, Pinia, VueUse, PrimeVue, vuedraggable, Tailwind CSS.

## Notable Issues
1. Duplicate tag-generation logic in `app.py` and `backend/images/tag.py`
2. No tests written yet
3. Mixed Python package managers (Pipfile + pyproject.toml)