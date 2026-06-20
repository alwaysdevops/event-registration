import pytest
from app import app, REGISTRATIONS

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Event Registration" in response.data

def test_successful_registration(client):
    REGISTRATIONS.clear()

    response = client.post(
        "/register",
        data={"name": "Alice", "email": "alice@example.com", "event_id": "1"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Thanks, Alice!" in response.data
    assert len(REGISTRATIONS) == 1
    assert REGISTRATIONS[0]["email"] == "alice@example.com"

def test_registration_missing_fields(client):
    response = client.post(
        "/register",
        data={"name": "", "email": "bob@example.com", "event_id": "1"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"All fields are required." in response.data
