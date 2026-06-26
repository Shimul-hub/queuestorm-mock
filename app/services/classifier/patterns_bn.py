from app.models.enums import CaseType
from app.services.classifier.patterns_en import PatternRule, _compile

BN_PATTERNS: list[PatternRule] = _compile(
    [
        (r"(ওটিপি|otp|পিন|পাসওয়ার্ড|পassword)", CaseType.PHISHING, 3.5),
        (r"(প্রতারণ|স্ক্যাম|জাল)", CaseType.PHISHING, 3.0),
        (r"(ভুল\s*নম্বর|ভুল\s*নম্বরে|ভুল\s*অ্যাকাউন্ট)", CaseType.WRONG_TRANSFER, 3.5),
        (r"(টাকা\s*পাঠ|পাঠিয়|ট্রান্সফার).{0,20}(ভুল)", CaseType.WRONG_TRANSFER, 3.0),
        (r"(পেমেন্ট\s*ব্যর্থ|লেনদেন\s*ব্যর্থ|transaction\s*fail)", CaseType.PAYMENT_FAILED, 3.0),
        (r"(ব্যালান্স\s*কেট|টাকা\s*কেট|balance\s*deduct)", CaseType.PAYMENT_FAILED, 3.0),
        (r"(রিফান্ড|টাকা\s*ফেরত|refund)", CaseType.REFUND_REQUEST, 2.5),
        (r"(মন\s*পাল্ট|cancel)", CaseType.REFUND_REQUEST, 2.0),
        (r"(অ্যাপ\s*ক্র্যাশ|crash|খুলছে\s*না)", CaseType.OTHER, 2.5),
    ]
)
