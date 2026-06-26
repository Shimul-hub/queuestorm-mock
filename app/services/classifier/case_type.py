from collections import defaultdict
from dataclasses import dataclass

from app.models.enums import CaseType
from app.services.classifier.patterns_banglish import BANGLISH_PATTERNS
from app.services.classifier.patterns_bn import BN_PATTERNS
from app.services.classifier.patterns_en import EN_PATTERNS, PatternRule


PRIORITY_ORDER: list[CaseType] = [
    CaseType.PHISHING,
    CaseType.WRONG_TRANSFER,
    CaseType.PAYMENT_FAILED,
    CaseType.REFUND_REQUEST,
    CaseType.OTHER,
]


@dataclass
class CaseTypeResult:
    case_type: CaseType
    scores: dict[CaseType, float]
    strong_hits: int
    cross_language_agreement: bool


def score_patterns(text: str, patterns: list[PatternRule]) -> dict[CaseType, float]:
    scores: dict[CaseType, float] = defaultdict(float)
    for rule in patterns:
        if rule.pattern.search(text):
            scores[rule.case_type] += rule.weight
    return scores


def detect_case_type(normalized_text: str, script_profile: str) -> CaseTypeResult:
    en_scores = score_patterns(normalized_text, EN_PATTERNS)
    bn_scores = score_patterns(normalized_text, BN_PATTERNS)
    banglish_scores = score_patterns(normalized_text, BANGLISH_PATTERNS)

    combined: dict[CaseType, float] = defaultdict(float)
    for bank in (en_scores, bn_scores, banglish_scores):
        for case_type, score in bank.items():
            combined[case_type] += score

    if not combined:
        return CaseTypeResult(
            case_type=CaseType.OTHER,
            scores={CaseType.OTHER: 0.0},
            strong_hits=0,
            cross_language_agreement=False,
        )

    top_score = max(combined.values())
    leaders = [ct for ct, score in combined.items() if score == top_score]

    if len(leaders) > 1:
        for case_type in PRIORITY_ORDER:
            if case_type in leaders:
                selected = case_type
                break
        else:
            selected = leaders[0]
    else:
        selected = leaders[0]

    strong_hits = sum(1 for score in combined.values() if score >= 2.5)
    cross_language_agreement = _has_cross_language_agreement(en_scores, bn_scores, banglish_scores, selected)

    return CaseTypeResult(
        case_type=selected,
        scores=dict(combined),
        strong_hits=strong_hits,
        cross_language_agreement=cross_language_agreement,
    )


def _has_cross_language_agreement(
    en_scores: dict[CaseType, float],
    bn_scores: dict[CaseType, float],
    banglish_scores: dict[CaseType, float],
    selected: CaseType,
) -> bool:
    banks_with_signal = 0
    for bank in (en_scores, bn_scores, banglish_scores):
        if bank.get(selected, 0) >= 2.0:
            banks_with_signal += 1
    return banks_with_signal >= 2
