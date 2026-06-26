from dataclasses import dataclass
from collections import defaultdict
import re

from app.models.enums import CaseType


@dataclass(frozen=True)
class PatternRule:
    pattern: re.Pattern[str]
    case_type: CaseType
    weight: float


def _compile(patterns: list[tuple[str, CaseType, float]]) -> list[PatternRule]:
    return [PatternRule(re.compile(p, re.I), ct, w) for p, ct, w in patterns]


EN_PATTERNS: list[PatternRule] = _compile(
    [
        (r"\b(otp|one[\s-]?time\s+password|pin\s+code|password|cvv|card\s+number)\b", CaseType.PHISHING, 3.0),
        (r"\b(scam|phish|social\s+engineering|fake\s+(call|sms|bkash|agent))\b", CaseType.PHISHING, 2.5),
        (r"\b(asking|asked|requested).{0,30}\b(otp|pin|password)\b", CaseType.PHISHING, 3.5),
        (r"\b(wrong|wrng)\s+(number|numbr|nombor|recipient|account|person|mobile)\b", CaseType.WRONG_TRANSFER, 3.0),
        (r"\b(sent|transfer(?:red)?|send).{0,40}\bwrong\b", CaseType.WRONG_TRANSFER, 3.5),
        (r"\b(mistaken|mistake).{0,20}\b(transfer|send|sent)\b", CaseType.WRONG_TRANSFER, 2.5),
        (r"\bpayment\s+failed\b", CaseType.PAYMENT_FAILED, 3.0),
        (r"\b(transaction\s+failed|failed\s+transaction)\b", CaseType.PAYMENT_FAILED, 2.5),
        (r"\b(balance\s+deducted|money\s+deducted|amount\s+deducted|charged)\b", CaseType.PAYMENT_FAILED, 2.5),
        (r"\b(failed).{0,30}\b(deducted|debited|taken)\b", CaseType.PAYMENT_FAILED, 3.0),
        (r"\brefund\b", CaseType.REFUND_REQUEST, 2.5),
        (r"\b(changed\s+my\s+mind|cancel\s+transaction|money\s+back)\b", CaseType.REFUND_REQUEST, 2.5),
        (r"\b(app\s+crash|crashed|not\s+opening|login\s+issue|bug)\b", CaseType.OTHER, 2.5),
        (r"\b(general|help|support|question)\b", CaseType.OTHER, 1.0),
    ]
)
