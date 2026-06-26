import re

_PHISHING_SIGNAL = re.compile(
    r"\b(otp|pin|password|scam|phish|fake\s+(call|sms|agent|bkash))\b",
    re.I,
)


def scan_input_risk(message: str) -> bool:
    return bool(_PHISHING_SIGNAL.search(message))
