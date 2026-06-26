# Submission Guide — Mock Preliminary Round

## Google Form Fields

| Field | What to submit |
|-------|----------------|
| Team name | Your registered team name |
| GitHub repository URL | `https://github.com/Shimul-hub/queuestorm-mock` |
| Live API base URL | `https://YOUR-SERVICE.onrender.com` (no trailing slash) |
| Deployment platform | Render |
| LLM used | Yes — OpenRouter (`meta-llama/llama-3.1-8b-instruct`) |
| Known issues or blockers | Optional |

## Before You Submit

```powershell
pytest -v
Invoke-RestMethod http://localhost:8000/health
```

After Render deploy:

```bash
curl https://YOUR-SERVICE.onrender.com/health
curl -X POST https://YOUR-SERVICE.onrender.com/sort-ticket \
  -H "Content-Type: application/json" \
  -d '{"ticket_id":"T-001","message":"I sent 3000 to wrong number"}'
```

## Render Setup Checklist

1. Connect Web Service to GitHub repo `Shimul-hub/queuestorm-mock`
2. Set environment variable `OPENROUTER_API_KEY` in Render Dashboard
3. Confirm health check path is `/health`
4. Deploy and copy public URL

See [RENDER_DEPLOY.md](RENDER_DEPLOY.md) for full steps.

## Docker Fallback (for judges)

```bash
cp .env.example judging.env
docker build -t queuestorm-mock .
docker run -p 8000:8000 --env-file judging.env queuestorm-mock
```

## Documentation Included for Judges

| File | Purpose |
|------|---------|
| `README.md` | Setup, API docs, samples, AI usage, safety, limitations |
| `.env.example` | Required environment variable names |
| `samples/request.json` | Sample request |
| `samples/response.json` | Sample response |
| `Dockerfile` | Docker fallback runbook |
| `render.yaml` | Render deployment configuration |
