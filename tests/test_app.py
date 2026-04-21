import pytest
from fastapi.testclient import TestClient

def test_root_redirect(client: TestClient):
    # Arrange
    # No specific setup needed

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert "/static/index.html" in response.headers["location"]

def test_get_activities(client: TestClient):
    # Arrange
    # Activities are pre-loaded in the app

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)

def test_signup_valid(client: TestClient):
    # Arrange
    email = "test@school.edu"

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    # Verify added
    activities_resp = client.get("/activities")
    assert email in activities_resp.json()["Chess Club"]["participants"]

def test_signup_activity_not_found(client: TestClient):
    # Arrange
    email = "test@school.edu"

    # Act
    response = client.post("/activities/NonExistent/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_signup_duplicate(client: TestClient):
    # Arrange
    email = "test@school.edu"
    client.post("/activities/Chess Club/signup", params={"email": email})  # First signup

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})  # Duplicate

    # Assert
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]

def test_signup_malformed_input(client: TestClient):
    # Arrange
    # Missing email

    # Act
    response = client.post("/activities/Chess Club/signup")

    # Assert
    assert response.status_code == 422  # Unprocessable Entity for missing required field

def test_unregister_valid(client: TestClient):
    # Arrange
    email = "test@school.edu"
    client.post("/activities/Chess Club/signup", params={"email": email})  # Signup first

    # Act
    response = client.delete("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]
    # Verify removed
    activities_resp = client.get("/activities")
    assert email not in activities_resp.json()["Chess Club"]["participants"]

def test_unregister_activity_not_found(client: TestClient):
    # Arrange
    email = "test@school.edu"

    # Act
    response = client.delete("/activities/NonExistent/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_unregister_not_signed_up(client: TestClient):
    # Arrange
    email = "notsigned@school.edu"

    # Act
    response = client.delete("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]

def test_unregister_malformed_input(client: TestClient):
    # Arrange
    # Missing email

    # Act
    response = client.delete("/activities/Chess Club/signup")

    # Assert
    assert response.status_code == 422  # Unprocessable Entity for missing required field
