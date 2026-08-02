from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_duplicate_signup_is_rejected():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 409
    assert response.json()["detail"] == "Student is already signed up"

    activities = client.get("/activities").json()
    assert activities[activity_name]["participants"].count(email) == 1


def test_participant_can_be_removed_from_activity():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_signup_updates_activity_participants():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200

    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]
