from app.models.enums import CaseType
from app.services.classifier.patterns_en import PatternRule, _compile

BANGLISH_PATTERNS: list[PatternRule] = _compile(
    [
        (r"\b(otp|pin|password)\s+(chay|chai|de|den|bolche|asked)\b", CaseType.PHISHING, 3.5),
        (r"\b(fake|scam)\s+(call|sms|bkash|agent)\b", CaseType.PHISHING, 3.0),
        (r"\bwrong\s+(nombor|number|account)\b", CaseType.WRONG_TRANSFER, 3.5),
        (r"\b(\d+)\s+(taka|tk).{0,20}wrong\b", CaseType.WRONG_TRANSFER, 3.0),
        (r"\bpayment\s+fail(ed)?\b", CaseType.PAYMENT_FAILED, 3.0),
        (r"\bbalance\s+(deducted|kata|kete)\b", CaseType.PAYMENT_FAILED, 3.0),
        (r"\brefund\s+(lagbe|chai|chay|den)\b", CaseType.REFUND_REQUEST, 2.5),
        (r"\bchanged\s+mind\b", CaseType.REFUND_REQUEST, 2.5),
        (r"\bapp\s+crash(ed)?\b", CaseType.OTHER, 2.5),
    ]
)
