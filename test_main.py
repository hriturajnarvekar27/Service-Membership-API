from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_member():
    response = client.post("/members/", json={
        "name": "Test User",
        "phone": "9999999999",
        "status": "active"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Test User"
