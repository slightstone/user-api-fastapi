import pytest
from fastapi.testclient import TestClient

from main import app  # adjust if your entrypoint is different

client = TestClient(app)


@pytest.fixture
def mock_firebase(monkeypatch):
    class MockFirebase:
        def __init__(self):
            self.users = {}

        def create_user(self, data):
            self.users["test_user_id"] = data
            return "test_user_id"

        def get_all_users(self):
            return self.users

        def get_user(self, user_id):
            return self.users.get(user_id)

        def update_user(self, user_id, updates):
            if user_id in self.users:
                self.users[user_id].update(updates)

        def delete_user(self, user_id):
            self.users.pop(user_id, None)

    mock = MockFirebase()
    monkeypatch.setattr("users.firebase.create_user", mock.create_user)
    monkeypatch.setattr("users.firebase.get_all_users", mock.get_all_users)
    monkeypatch.setattr("users.firebase.get_user", mock.get_user)
    monkeypatch.setattr("users.firebase.update_user", mock.update_user)
    monkeypatch.setattr("users.firebase.delete_user", mock.delete_user)
    return mock


@pytest.fixture
def mock_fetch_location(monkeypatch):
    monkeypatch.setattr(
        "users.geocode.fetch_location_from_zip",
        lambda zip_code: type(
            "Location",
            (),
            {
                "coord": type("Coord", (), {"lat": "40.75", "lon": "-73.99"})(),
                "timezone_offset_seconds": -18000,
                "timezone_human_readable": "America/New_York",
                "timezone_error": False,
            },
        )(),
    )


def test_list_users(mock_firebase):
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == {}


def test_get_user_existing(mock_firebase):
    mock_firebase.create_user(
        {
            "name": "Test",
            "zip_code": "10001",
            "latitude": "40.75",
            "longitude": "-73.99",
            "timezone_offset_seconds": -18000,
            "timezone": "America/New_York",
            "timezone_error": False,
        }
    )

    response = client.get("/users/test_user_id")
    assert response.status_code == 200
    assert response.json()["name"] == "Test"


def test_get_user_not_found(mock_firebase):
    response = client.get("/users/does_not_exist")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_update_user_with_zip(mock_firebase, mock_fetch_location):
    mock_firebase.create_user(
        {
            "name": "Test",
            "zip_code": "10001",
            "latitude": "40.75",
            "longitude": "-73.99",
            "timezone_offset_seconds": -18000,
            "timezone": "America/New_York",
            "timezone_error": False,
        }
    )

    response = client.put("/users/test_user_id", json={"zip_code": "10002"})
    assert response.status_code == 200
    assert response.json() == {"updated": True}


def test_delete_user(mock_firebase):
    mock_firebase.create_user(
        {
            "name": "Test",
            "zip_code": "10001",
            "latitude": "40.75",
            "longitude": "-73.99",
            "timezone_offset_seconds": -18000,
            "timezone": "America/New_York",
            "timezone_error": False,
        }
    )

    response = client.delete("/users/test_user_id")
    assert response.status_code == 200
    assert response.json() == {"deleted": True}
