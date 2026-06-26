from app.models.enums import CaseType
from app.services.normalizer.text import extract_amount


def generate_summary(case_type: CaseType, raw_message: str, normalized_text: str) -> str:
    amount = extract_amount(normalized_text) or extract_amount(raw_message)
    amount_text = f"{amount} BDT" if amount else "funds"

    templates: dict[CaseType, str] = {
        CaseType.WRONG_TRANSFER: (
            f"Customer reports sending {amount_text} to the wrong recipient and requests recovery assistance."
            if amount
            else "Customer reports a wrong transfer and requests recovery assistance."
        ),
        CaseType.PAYMENT_FAILED: (
            "Customer reports a failed payment where the balance may have been deducted."
        ),
        CaseType.REFUND_REQUEST: (
            f"Customer requests a refund related to a recent transaction of {amount_text}."
            if amount
            else "Customer requests a refund for a recent transaction."
        ),
        CaseType.PHISHING: (
            "Customer reports a suspicious contact requesting sensitive verification details."
        ),
        CaseType.OTHER: (
            "Customer reports a general application or service issue requiring support review."
        ),
    }
    return templates[case_type]
