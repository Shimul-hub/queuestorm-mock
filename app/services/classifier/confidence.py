from app.models.enums import CaseType
from app.services.classifier.case_type import CaseTypeResult


def compute_confidence(
    case_result: CaseTypeResult,
    message_length: int,
) -> float:
    confidence = 0.55

    confidence += min(case_result.strong_hits * 0.15, 0.30)

    scores = sorted(case_result.scores.values(), reverse=True)
    if len(scores) >= 2 and (scores[0] - scores[1]) > 2.0:
        confidence += 0.10
    elif len(scores) >= 2 and (scores[0] - scores[1]) <= 1.0:
        confidence -= 0.15

    if case_result.cross_language_agreement:
        confidence += 0.05

    if message_length < 10:
        confidence -= 0.10
    elif message_length > 2000:
        confidence -= 0.10

    if case_result.case_type == CaseType.OTHER and max(scores, default=0) < 1.5:
        confidence -= 0.10

    return round(max(0.0, min(1.0, confidence)), 2)
