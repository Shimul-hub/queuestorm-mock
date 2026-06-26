import re

from app.models.enums import CaseType, Severity

_CONTESTED_REFUND = re.compile(
    r"\b(unauthorized|didn['']t\s+make|not\s+mine|dispute|contested|chargeback|fraudulent)\b",
    re.I,
)
_URGENCY = re.compile(r"\b(urgent|immediately|asap|emergency|now)\b", re.I)
_AMOUNT = re.compile(r"\d+")


def evaluate_severity(case_type: CaseType, normalized_text: str) -> Severity:
    if case_type == CaseType.PHISHING:
        return Severity.CRITICAL

    if case_type == CaseType.WRONG_TRANSFER:
        if _AMOUNT.search(normalized_text) or _URGENCY.search(normalized_text):
            return Severity.HIGH
        return Severity.HIGH

    if case_type == CaseType.PAYMENT_FAILED:
        return Severity.HIGH

    if case_type == CaseType.REFUND_REQUEST:
        if _CONTESTED_REFUND.search(normalized_text):
            return Severity.MEDIUM
        return Severity.LOW

    return Severity.LOW
