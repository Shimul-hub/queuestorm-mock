# QueueStorm Mock API

Backend API for **Codex Community Hackathon 2026** — Mock Preliminary Round.

Classifies customer support tickets via `POST /sort-ticket` with evidence-based rules, multilingual support (EN / BN / mixed / Banglish), optional OpenRouter LLM fallback, and safety guardrails.

**Live deployment:** Render (primary) · **Fallback:** Docker · **Repo:** [github.com/Shimul-hub/queuestorm-mock](https://github.com/Shimul-hub/queuestorm-mock)

---

## For Judges — Quick Start

### Option A: Call the live endpoint (preferred)

```
GET  https://YOUR-SERVICE.onrender.com/health
POST https://YOUR-SERVICE.onrender.com/sort-ticket
```

No login required. JSON in, JSON out.

### Option B: Docker fallback

```bash
git clone https://github.com/Shimul-hub/queuestorm-mock.git
cd queuestorm-mock
cp .env.example judging.env
# Optional: set OPENROUTER_API_KEY in judging.env for LLM fallback testing
docker build -t queuestorm-mock .
docker run -p 8000:8000 --env-file judging.env queuestorm-mock
curl http://localhost:8000/health
```

Image size: ~304MB (under 500MB guideline). Binds `0.0.0.0:8000`. No GPU.

### Option C: Run locally

See [Local Setup](#local-setup) below.

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Returns `{"status":"ok"}` |
| POST | `/sort-ticket` | Classifies one support ticket |
| GET | `/docs` | Swagger UI (local testing only) |

---

## Sample Request

See [`samples/request.json`](samples/request.json):

```json
{
  "ticket_id": "T-001",
  "channel": "app",
  "locale": "en",
  "message": "I sent 5000 taka to a wrong number this morning, please help me get it back"
}
```

Bengali example: [`samples/request_bengali.json`](samples/request_bengali.json)

## Sample Response

See [`samples/response.json`](samples/response.json):

```json
{
  "ticket_id": "T-001",
  "case_type": "wrong_transfer",
  "severity": "high",
  "department": "dispute_resolution",
  "agent_summary": "Customer reports sending 5000 BDT to the wrong recipient and requests recovery assistance.",
  "human_review_required": false,
  "confidence": 0.85
}
```

---

## Public Sample Cases (Expected Behaviour)

| # | Message | case_type | severity | department | human_review |
|---|---------|-----------|----------|------------|--------------|
| 1 | I sent 3000 to wrong number | wrong_transfer | high | dispute_resolution | false |
| 2 | Payment failed but balance deducted | payment_failed | high | payments_ops | false |
| 3 | Someone called asking my OTP, is that bKash? | phishing_or_social_engineering | critical | fraud_risk | **true** |
| 4 | Please refund my last transaction, I changed my mind | refund_request | low | customer_support | false |
| 5 | App crashed when I opened it | other | low | customer_support | false |

---

## Architecture

```
POST /sort-ticket
  → Pydantic validation
  → Multilingual normalization (EN + BN + Banglish)
  → Rule engine (case type, severity, department, confidence)
  → OpenRouter fallback if confidence < 0.70
  → Safety sanitizer on agent_summary
  → Structured JSON response
```

---

## AI / Model Usage

| Component | Approach |
|-----------|----------|
| Primary | Deterministic rule engine with weighted pattern banks |
| Fallback | OpenRouter API when rule confidence < 0.70 |
| Model | `meta-llama/llama-3.1-8b-instruct` (verified on OpenRouter) |
| Authority | Backend validates all LLM output; unsafe text replaced with templates |
| Without API key | Rules-only mode still returns valid JSON for all public samples |

---

## Safety Logic

- `agent_summary` **never** requests PIN, OTP, password, or card numbers
- **Never** promises refunds, approvals, or unauthorized account actions
- `human_review_required = true` when `severity == critical` OR `case_type == phishing_or_social_engineering`
- Output sanitizer strips unsafe phrasing before every response
- Errors return generic messages — no stack traces or secrets in responses

---

## Environment Variables

Copy [`.env.example`](.env.example) to `.env` locally or set in Render Dashboard.

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8000` | Set by Render automatically in production |
| `OPENROUTER_API_KEY` | empty | OpenRouter key (secret — not in repo) |
| `OPENROUTER_MODEL` | `meta-llama/llama-3.1-8b-instruct` | LLM fallback model |
| `LLM_ENABLED` | `true` | Enable LLM fallback |
| `LLM_CONFIDENCE_THRESHOLD` | `0.70` | Skip LLM when rules are confident enough |
| `LLM_TIMEOUT_SECONDS` | `8` | OpenRouter timeout |
| `LOG_LEVEL` | `INFO` | Logging level |

---

## Local Setup

### Prerequisites

- Python 3.12+
- Optional: Docker Desktop

### Install and run

```powershell
cd "g:\Sust Hackathon"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Verify locally

- Browser: `http://localhost:8000/docs` (paste Bengali in request body)
- PowerShell:

```powershell
Invoke-RestMethod http://localhost:8000/health
Invoke-RestMethod http://localhost:8000/sort-ticket -Method POST -ContentType "application/json" -Body '{"ticket_id":"T-001","message":"I sent 3000 to wrong number"}'
```

### Run tests

```powershell
pytest -v
```

Expected: **19 passed**

---

## Render Deployment

Full steps: [`docs/RENDER_DEPLOY.md`](docs/RENDER_DEPLOY.md)

Summary:

1. Connect Render Web Service to `Shimul-hub/queuestorm-mock` on GitHub
2. Build: `pip install -r requirements.txt`
3. Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Set `OPENROUTER_API_KEY` in Render Environment (secret)
5. Health check path: `/health`

Included [`render.yaml`](render.yaml) documents the same settings for Blueprint deploy.

---

## Docker Fallback (Judges)

```powershell
docker build -t queuestorm-mock .
copy .env.example judging.env
# Edit judging.env — add OPENROUTER_API_KEY if testing LLM path
docker run -p 8000:8000 --env-file judging.env queuestorm-mock
```

Rules-only mode works without `OPENROUTER_API_KEY`.

---

## Known Limitations

- Ambiguous multi-issue tickets route by priority: phishing > wrong_transfer > payment_failed > refund > other
- Banglish coverage uses curated romanization patterns; rare spellings may trigger LLM fallback
- Render free tier may cold-start; first `/health` request can take 30–60 seconds
- LLM fallback requires valid OpenRouter key and outbound network access

---

## Project Structure

```
app/           # FastAPI application
tests/         # pytest suite (19 tests)
samples/       # Sample request/response JSON for judges
docs/          # PRD, submission checklist, Render guide
render.yaml    # Render Blueprint configuration
Dockerfile     # Docker fallback (<500MB)
requirements.txt
.env.example   # Variable names only — no secrets
```

---

## Submission Checklist

- [ ] Public HTTPS endpoint on Render responds to `/health`
- [ ] GitHub repo public with this README
- [ ] All 5 public sample cases pass
- [ ] `.env.example` present; no secrets in repository
- [ ] Google Form: repo URL, Render URL, platform=Render, LLM usage documented
