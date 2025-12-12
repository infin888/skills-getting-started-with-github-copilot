import copy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture()
def client():
    return TestClient(app_module.app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset in-memory activities between tests to avoid cross-test leakage."""
    original = copy.deepcopy(app_module.activities)
    try:
        yield
    finally:
        app_module.activities.clear()
        app_module.activities.update(copy.deepcopy(original))


def test_root_redirects_to_static_index(client: TestClient):
    resp = client.get("/", follow_redirects=False)
    assert resp.status_code == 302
    assert resp.headers["location"] == "/static/index.html"


def test_get_activities_returns_expected_shape(client: TestClient):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()

    assert isinstance(data, dict)
    assert "Chess Club" in data

    chess = data["Chess Club"]
    assert set(chess.keys()) >= {"description", "schedule", "max_participants", "participants"}
    assert isinstance(chess["participants"], list)


def test_signup_adds_participant_and_normalizes_email(client: TestClient):
    # Ensure unique email for this test
    email = "NewStudent@Mergington.edu"
    activity = "Chess Club"

    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200

    # Email should be normalized to lowercase
    activities = client.get("/activities").json()
    assert "newstudent@mergington.edu" in activities[activity]["participants"]


def test_signup_duplicate_returns_409(client: TestClient):
    email = "dup@mergington.edu"
    activity = "Chess Club"

    first = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert first.status_code == 200

    second = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert second.status_code == 409


def test_delete_unregister_removes_participant(client: TestClient):
    activity = "Chess Club"
    email = "remove-me@mergington.edu"

    client.post(f"/activities/{activity}/signup", params={"email": email})

    resp = client.delete(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200

    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]


def test_delete_unregister_unknown_returns_404(client: TestClient):
    resp = client.delete("/activities/Chess%20Club/signup", params={"email": "not-registered@mergington.edu"})
    assert resp.status_code == 404


def test_unknown_activity_returns_404(client: TestClient):
    resp = client.post("/activities/Does%20Not%20Exist/signup", params={"email": "a@mergington.edu"})
    assert resp.status_code == 404
