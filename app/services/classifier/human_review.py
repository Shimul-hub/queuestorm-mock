from app.models.enums import CaseType, Severity


def requires_human_review(case_type: CaseType, severity: Severity) -> bool:
    if case_type == CaseType.PHISHING:
        return True
    return severity == Severity.CRITICAL
