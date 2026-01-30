import copy
from src import app as app_module
# Estado inicial das atividades para reset
INITIAL_ACTIVITIES = copy.deepcopy(app_module.activities)

import pytest

@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(INITIAL_ACTIVITIES))
import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball" in data

def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Basketball"
    # Remove if already present
    client.delete(f"/activities/{activity}/participants/{email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Try duplicate signup
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400
    # Clean up
    client.delete(f"/activities/{activity}/participants/{email}")

def test_remove_participant():
    email = "removeuser@mergington.edu"
    activity = "Soccer Club"
    # Remove if already present
    client.delete(f"/activities/{activity}/participants/{email}")
    # Add
    add_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert add_resp.status_code == 200
    # Remove
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" in response.json()["message"]
    # Try removing again
    response2 = client.delete(f"/activities/{activity}/participants/{email}")
    assert response2.status_code == 404
