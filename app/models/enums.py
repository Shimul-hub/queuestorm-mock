from enum import StrEnum


class CaseType(StrEnum):
    WRONG_TRANSFER = "wrong_transfer"
    PAYMENT_FAILED = "payment_failed"
    REFUND_REQUEST = "refund_request"
    PHISHING = "phishing_or_social_engineering"
    OTHER = "other"


class Severity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Department(StrEnum):
    CUSTOMER_SUPPORT = "customer_support"
    DISPUTE_RESOLUTION = "dispute_resolution"
    PAYMENTS_OPS = "payments_ops"
    FRAUD_RISK = "fraud_risk"


class Channel(StrEnum):
    APP = "app"
    SMS = "sms"
    CALL_CENTER = "call_center"
    MERCHANT_PORTAL = "merchant_portal"


class Locale(StrEnum):
    BN = "bn"
    EN = "en"
    MIXED = "mixed"
