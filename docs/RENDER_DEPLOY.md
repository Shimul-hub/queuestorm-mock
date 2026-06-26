# Render Deployment Guide

Connect your existing Render Web Service to this GitHub repository.

## 1. Push code to GitHub

Repository: `https://github.com/Shimul-hub/queuestorm-mock`

## 2. Connect Render to GitHub

1. Open [dashboard.render.com](https://dashboard.render.com)
2. Open your **Web Service** (or create one)
3. **Settings → Build & Deploy**
4. **Connect repository** → select `Shimul-hub/queuestorm-mock`
5. Branch: `main`

## 3. Render settings (must match)

| Setting | Value |
|---------|-------|
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| Health Check Path | `/health` |

Or use the included [`render.yaml`](../render.yaml) Blueprint if deploying via Blueprint.

## 4. Environment variables (Render Dashboard → Environment)

Set these in the Render UI — **never commit real secrets to GitHub**.

| Key | Value |
|-----|-------|
| `OPENROUTER_API_KEY` | Your OpenRouter key (secret) |
| `OPENROUTER_MODEL` | `meta-llama/llama-3.1-8b-instruct` |
| `LLM_ENABLED` | `true` |
| `LLM_CONFIDENCE_THRESHOLD` | `0.70` |
| `LLM_TIMEOUT_SECONDS` | `8` |
| `LOG_LEVEL` | `INFO` |

Render injects `PORT` automatically — do not hardcode it.

## 5. Deploy and verify

After deploy completes, test your public URL (example: `https://queuestorm-mock.onrender.com`):

```bash
curl https://YOUR-SERVICE.onrender.com/health
curl -X POST https://YOUR-SERVICE.onrender.com/sort-ticket \
  -H "Content-Type: application/json" \
  -d '{"ticket_id":"T-001","message":"I sent 3000 to wrong number"}'
```

**Note:** Free tier may cold-start (~30–60s on first request). Hit `/health` once before judging.

## 6. Submit to Google Form

- **GitHub URL:** `https://github.com/Shimul-hub/queuestorm-mock`
- **Live API base URL:** `https://YOUR-SERVICE.onrender.com` (no trailing slash)
- **Deployment platform:** Render
- **LLM used:** Yes — OpenRouter (`meta-llama/llama-3.1-8b-instruct`)
