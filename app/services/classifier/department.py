import re

from app.models.enums import CaseType, Department, Severity

_CONTESTED_REFUND = re.compile(
    r"\b(unauthorized|didn['']t\s+make|not\s+mine|dispute|contested|chargeback|fraudulent)\b",
    re.I,
)


def map_department(case_type: CaseType, severity: Severity, normalized_text: str) -> Department:
    if case_type == CaseType.PHISHING:
        return Department.FRAUD_RISK
    if case_type == CaseType.WRONG_TRANSFER:
        return Department.DISPUTE_RESOLUTION
    if case_type == CaseType.PAYMENT_FAILED:
        return Department.PAYMENTS_OPS
    if case_type == CaseType.REFUND_REQUEST:
        if _CONTESTED_REFUND.search(normalized_text):
            return Department.DISPUTE_RESOLUTION
        if severity == Severity.LOW:
            return Department.CUSTOMER_SUPPORT
        return Department.DISPUTE_RESOLUTION
    return Department.CUSTOMER_SUPPORT
