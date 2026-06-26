import re

_BANGLISH_REPLACEMENTS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bb[\-\s]?kash\b", re.I), "bkash"),
    (re.compile(r"\botp\b|\botip\b|\b[o0]tp\b", re.I), "otp"),
    (re.compile(r"\bpin\b|\bpin\s*code\b", re.I), "pin"),
    (re.compile(r"\bvul\b|\bvool\b|\bvl\b", re.I), "wrong"),
    (re.compile(r"\bnombor\b|\bnmbr\b|\bnumber\b", re.I), "number"),
    (re.compile(r"\btaka\b|\btk\b|\bbdt\b", re.I), "taka"),
    (re.compile(r"\brefund\b|\brefund\s+chai\b|\brefund\s+lagbe\b", re.I), "refund"),
    (re.compile(r"\bbalance\s+kata\b|\bbalance\s+kete\b", re.I), "balance deducted"),
    (re.compile(r"\bprotarona\b|\bscam\b|\bfake\b", re.I), "scam"),
    (re.compile(r"\bapp\s+crash\b|\bcrash\b", re.I), "app crash"),
    (re.compile(r"\bchanged\s+mind\b|\bmane\s+change\b", re.I), "changed mind"),
]


def normalize_banglish(text: str) -> str:
    normalized = text
    for pattern, replacement in _BANGLISH_REPLACEMENTS:
        normalized = pattern.sub(replacement, normalized)
    return normalized
