"""Verify OpenRouter models work with our classification prompt."""
import asyncio
import json
import os
import time

import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ["OPENROUTER_API_KEY"]
MODELS = [
    "google/gemini-2.0-flash-001",
    "google/gemini-2.0-flash-lite-001",
    "google/gemini-flash-1.5",
    "meta-llama/llama-3.1-8b-instruct",
    "openai/gpt-4o-mini",
    "mistralai/mistral-7b-instruct",
    "qwen/qwen-2.5-7b-instruct",
]

PROMPT = """Return ONLY JSON:
{"case_type":"wrong_transfer","severity":"high","department":"dispute_resolution","agent_summary":"Customer reports wrong transfer.","human_review_required":false,"confidence":0.85}
Classify: I sent money to wrong number but wording is unclear"""


async def test_model(client: httpx.AsyncClient, model: str) -> tuple[str, bool, float, str]:
    start = time.perf_counter()
    try:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": PROMPT}],
                "temperature": 0.1,
                "response_format": {"type": "json_object"},
            },
            timeout=10.0,
        )
        elapsed = time.perf_counter() - start
        if response.status_code != 200:
            return model, False, elapsed, f"HTTP {response.status_code}: {response.text[:120]}"
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        required = {
            "case_type",
            "severity",
            "department",
            "agent_summary",
            "human_review_required",
            "confidence",
        }
        if not required.issubset(parsed.keys()):
            return model, False, elapsed, f"missing fields: {parsed.keys()}"
        return model, True, elapsed, "ok"
    except Exception as exc:
        elapsed = time.perf_counter() - start
        return model, False, elapsed, str(exc)[:120]


async def main() -> None:
    async with httpx.AsyncClient() as client:
        print("Testing OpenRouter models...\n")
        working: list[tuple[str, float]] = []
        for model in MODELS:
            name, ok, elapsed, detail = await test_model(client, model)
            status = "PASS" if ok else "FAIL"
            print(f"{status} {name} ({elapsed:.2f}s) - {detail}")
            if ok:
                working.append((name, elapsed))
        if working:
            best = min(working, key=lambda x: x[1])
            print(f"\nRecommended model: {best[0]} ({best[1]:.2f}s)")
        else:
            print("\nNo working models found.")


if __name__ == "__main__":
    asyncio.run(main())
