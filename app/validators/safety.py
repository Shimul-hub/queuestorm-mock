import re

_CREDENTIAL_REQUEST = re.compile(
    r"\b("
    r"share\s+(your\s+)?(pin|otp|password|cvv|card\s+number)"
    r"|provide\s+(your\s+)?(pin|otp|password)"
    r"|send\s+(your\s+)?(pin|otp|password)"
    r"|enter\s+(your\s+)?(pin|otp|password)"
    r")\b",
    re.I,
)

_UNAUTHORIZED_PROMISE = re.compile(
    r"\b("
    r"we\s+will\s+(refund|approve|recover|return|block)"
    r"|has\s+been\s+(refunded|approved|recovered|blocked)"
    r"|guaranteed\s+(refund|recovery|approval)"
    r"|will\s+immediately\s+(refund|approve|recover)"
    r")\b",
    re.I,
)

_SENSITIVE_TERMS = re.compile(r"\b(pin|otp|password|cvv|card\s+number)\b", re.I)


def scan_input_risk(message: str) -> bool:
    return bool(_SENSITIVE_TERMS.search(message))


def sanitize_summary(summary: str) -> str:
    cleaned = summary.strip()
    cleaned = _CREDENTIAL_REQUEST.sub("contact official support channels", cleaned)
    cleaned = _UNAUTHORIZED_PROMISE.sub("requires review by the support team", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if not cleaned.endswith("."):
        cleaned += "."
    return cleaned


def is_summary_safe(summary: str) -> bool:
    return not _CREDENTIAL_REQUEST.search(summary) and not _UNAUTHORIZED_PROMISE.search(summary)
