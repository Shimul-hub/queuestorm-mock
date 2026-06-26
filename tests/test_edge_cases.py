def test_missing_optional_fields(client):
    response = client.post(
        "/sort-ticket",
        json={"ticket_id": "T-002", "message": "App crashed when I opened it"},
    )
    assert response.status_code == 200


def test_invalid_optional_enums_ignored(client):
    response = client.post(
        "/sort-ticket",
        json={
            "ticket_id": "T-003",
            "channel": "invalid_channel",
            "locale": "fr",
            "message": "App crashed when I opened it",
        },
    )
    assert response.status_code == 200


def test_missing_required_field_returns_422(client):
    response = client.post("/sort-ticket", json={"ticket_id": "T-004"})
    assert response.status_code == 422


def test_invalid_json_returns_422(client):
    response = client.post(
        "/sort-ticket",
        data="not-json",
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 422


def test_oversized_message_returns_422(client):
    response = client.post(
        "/sort-ticket",
        json={"ticket_id": "T-005", "message": "x" * 5001},
    )
    assert response.status_code == 422


def test_typo_wrong_number(client):
    response = client.post(
        "/sort-ticket",
        json={"ticket_id": "T-006", "message": "I sent 3000 to wrng numbr"},
    )
    data = response.json()
    assert response.status_code == 200
    assert data["case_type"] == "wrong_transfer"


def test_response_has_all_required_fields(client):
    response = client.post(
        "/sort-ticket",
        json={"ticket_id": "T-007", "message": "App crashed when I opened it"},
    )
    data = response.json()
    for field in (
        "ticket_id",
        "case_type",
        "severity",
        "department",
        "agent_summary",
        "human_review_required",
        "confidence",
    ):
        assert field in data
        assert data[field] is not None
