from app.models.enums import CaseType, Department, Severity


def test_bengali_wrong_transfer(client):
    response = client.post(
        "/sort-ticket",
        json={
            "ticket_id": "T-BN-1",
            "locale": "bn",
            "message": "আমি ভুল নম্বরে ৩০০০ টাকা পাঠিয়েছি",
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data["case_type"] == CaseType.WRONG_TRANSFER.value
    assert data["severity"] == Severity.HIGH.value
    assert data["department"] == Department.DISPUTE_RESOLUTION.value


def test_banglish_phishing(client):
    response = client.post(
        "/sort-ticket",
        json={
            "ticket_id": "T-BG-1",
            "locale": "mixed",
            "message": "ekjon fake bkash agent amar otp chay, eta ki scam?",
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data["case_type"] == CaseType.PHISHING.value
    assert data["severity"] == Severity.CRITICAL.value
    assert data["human_review_required"] is True


def test_mixed_payment_failed(client):
    response = client.post(
        "/sort-ticket",
        json={
            "ticket_id": "T-MX-1",
            "locale": "mixed",
            "message": "payment fail hoise kintu balance kete nise",
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data["case_type"] == CaseType.PAYMENT_FAILED.value
    assert data["department"] == Department.PAYMENTS_OPS.value


def test_english_refund_banglish(client):
    response = client.post(
        "/sort-ticket",
        json={
            "ticket_id": "T-BG-2",
            "message": "amar last transaction er refund lagbe, mane change korechi",
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data["case_type"] == CaseType.REFUND_REQUEST.value
    assert data["severity"] == Severity.LOW.value
