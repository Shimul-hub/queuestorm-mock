import pytest

from app.models.enums import CaseType, Department, Severity


@pytest.mark.parametrize(
    ("message", "case_type", "severity", "department", "human_review"),
    [
        (
            "I sent 3000 to wrong number",
            CaseType.WRONG_TRANSFER,
            Severity.HIGH,
            Department.DISPUTE_RESOLUTION,
            False,
        ),
        (
            "Payment failed but balance deducted",
            CaseType.PAYMENT_FAILED,
            Severity.HIGH,
            Department.PAYMENTS_OPS,
            False,
        ),
        (
            "Someone called asking my OTP, is that bKash?",
            CaseType.PHISHING,
            Severity.CRITICAL,
            Department.FRAUD_RISK,
            True,
        ),
        (
            "Please refund my last transaction, I changed my mind",
            CaseType.REFUND_REQUEST,
            Severity.LOW,
            Department.CUSTOMER_SUPPORT,
            False,
        ),
        (
            "App crashed when I opened it",
            CaseType.OTHER,
            Severity.LOW,
            Department.CUSTOMER_SUPPORT,
            False,
        ),
    ],
)
def test_public_sample_cases(client, message, case_type, severity, department, human_review):
    response = client.post(
        "/sort-ticket",
        json={"ticket_id": "T-001", "message": message},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ticket_id"] == "T-001"
    assert data["case_type"] == case_type.value
    assert data["severity"] == severity.value
    assert data["department"] == department.value
    assert data["human_review_required"] is human_review
    assert 0.0 <= data["confidence"] <= 1.0
    assert data["agent_summary"]
