# Product Requirements Document — QueueStorm Mock API

## Project

Codex Community Hackathon 2026 — Mock Preliminary Round

## Deployment

- **Primary:** Render Web Service (GitHub-connected)
- **Fallback:** Docker (`Dockerfile`, image <500MB)
- **Repository:** https://github.com/Shimul-hub/queuestorm-mock

## Endpoints

| Method | Path | Response |
|--------|------|----------|
| GET | `/health` | `{"status":"ok"}` |
| POST | `/sort-ticket` | Structured classification JSON |

## AI Strategy

- Rules-first hybrid classifier
- OpenRouter fallback when confidence < 0.70
- Model: `meta-llama/llama-3.1-8b-instruct`

## Decision Log

- Deployment switched from AWS EC2 to Render (mock + preliminary)
- Core API logic unchanged — local tests pass
- Docker retained as judge fallback

## Judge Documentation Requirements (met)

- README: setup, run commands, AI usage, safety logic, limitations
- Sample request/response in `samples/` and README
- `.env.example` with placeholder values only
- Docker build/run instructions for fallback path
