"""Benchmark API latency for competition SLA (30s timeout, target <5s p95)."""
import asyncio
import statistics
import time

import httpx

BASE = "http://localhost:8001"
CASES = [
    ("rules_wrong_transfer", {"ticket_id": "L1", "message": "I sent 3000 to wrong number"}),
    ("rules_phishing", {"ticket_id": "L2", "message": "Someone called asking my OTP, is that bKash?"}),
    (
        "llm_ambiguous",
        {"ticket_id": "L3", "message": "something went wrong with my money thing yesterday maybe"},
    ),
]


async def bench_case(client: httpx.AsyncClient, name: str, payload: dict) -> tuple[str, float, int]:
    start = time.perf_counter()
    response = await client.post(f"{BASE}/sort-ticket", json=payload, timeout=30.0)
    elapsed = time.perf_counter() - start
    return name, elapsed, response.status_code


async def main() -> None:
    async with httpx.AsyncClient() as client:
        health_start = time.perf_counter()
        health = await client.get(f"{BASE}/health", timeout=10.0)
        health_ms = (time.perf_counter() - health_start) * 1000
        print(f"Health: {health.status_code} in {health_ms:.0f}ms")

        timings: dict[str, list[float]] = {name: [] for name, _ in CASES}
        for _ in range(3):
            for name, payload in CASES:
                _, elapsed, status = await bench_case(client, name, payload)
                timings[name].append(elapsed)
                print(f"{name}: {elapsed:.3f}s status={status}")

        print("\nSummary (seconds):")
        for name, values in timings.items():
            print(f"  {name}: max={max(values):.3f}s avg={statistics.mean(values):.3f}s")
        overall_max = max(v for vals in timings.values() for v in vals)
        print(f"\nOverall max: {overall_max:.3f}s (SLA limit: 30s)")
        if overall_max <= 5.0:
            print("PASS: within 5s p95 target band")
        elif overall_max <= 30.0:
            print("PASS: within 30s hard timeout")


if __name__ == "__main__":
    asyncio.run(main())
