import re
import unicodedata

_BENGALI_RANGE = re.compile(r"[\u0980-\u09FF]")
_LATIN_RANGE = re.compile(r"[A-Za-z]")


def normalize_text(raw: str) -> str:
    text = unicodedata.normalize("NFKC", raw)
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text


def detect_script_profile(text: str) -> str:
    has_bn = bool(_BENGALI_RANGE.search(text))
    has_en = bool(_LATIN_RANGE.search(text))
    if has_bn and has_en:
        return "mixed"
    if has_bn:
        return "bn"
    return "en"


def extract_amount(text: str) -> str | None:
    patterns = [
        r"(\d+(?:[,\.]\d+)?)\s*(?:bdt|taka|tk|টাকা)",
        r"(?:sent|transfer(?:red)?|paid|send)\s+(\d+(?:[,\.]\d+)?)",
        r"(\d+(?:[,\.]\d+)?)\s+(?:to|number|nombor|নম্বর)",
        r"(\d+(?:[,\.]\d+)?)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).replace(",", "")
    return None
