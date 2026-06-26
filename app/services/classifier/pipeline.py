from dataclasses import dataclass

from app.models.enums import CaseType, Department, Severity
from app.services.classifier.case_type import CaseTypeResult, detect_case_type
from app.services.classifier.confidence import compute_confidence
from app.services.classifier.department import map_department
from app.services.classifier.human_review import requires_human_review
from app.services.classifier.severity import evaluate_severity
from app.services.normalizer.banglish import normalize_banglish
from app.services.normalizer.text import detect_script_profile, normalize_text


@dataclass
class ClassificationResult:
    case_type: CaseType
    severity: Severity
    department: Department
    human_review_required: bool
    confidence: float
    normalized_text: str
    script_profile: str
    case_result: CaseTypeResult


def classify_message(raw_message: str) -> ClassificationResult:
    normalized = normalize_text(raw_message)
    normalized = normalize_banglish(normalized)
    script_profile = detect_script_profile(raw_message)

    case_result = detect_case_type(normalized, script_profile)
    severity = evaluate_severity(case_result.case_type, normalized)
    department = map_department(case_result.case_type, severity, normalized)
    human_review = requires_human_review(case_result.case_type, severity)
    confidence = compute_confidence(case_result, len(raw_message))

    return ClassificationResult(
        case_type=case_result.case_type,
        severity=severity,
        department=department,
        human_review_required=human_review,
        confidence=confidence,
        normalized_text=normalized,
        script_profile=script_profile,
        case_result=case_result,
    )
