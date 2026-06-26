import re

from app.validators.safety import is_summary_safe, sanitize_summary


def test_summary_never_requests_credentials(client):
    messages = [
        "Someone called asking my OTP, is that bKash?",
        "I sent 3000 to wrong number",
        "Payment failed but balance deducted",
        "Please refund my last transaction, I changed my mind",
        "App crashed when I opened it",
        "ekjon fake bkash agent amar otp chay",
    ]
    blocked = re.compile(r"\b(share|provide|send|enter)\s+(your\s+)?(pin|otp|password)\b", re.I)
    for message in messages:
        response = client.post("/sort-ticket", json={"ticket_id": "T-S", "message": message})
        summary = response.json()["agent_summary"]
        assert not blocked.search(summary)


def test_sanitize_removes_unsafe_phrases():
    unsafe = "Please share your OTP so we can verify your account."
    cleaned = sanitize_summary(unsafe)
    assert is_summary_safe(cleaned)
    assert "share your OTP" not in cleaned.lower()
