import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    # Reset activities dict before each test to ensure isolation
    original = activities.copy()
    yield
    activities.clear()
    activities.update(original)
