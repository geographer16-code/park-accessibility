from fastapi.testclient import TestClient
from park_access.service import app

client = TestClient(app)


def test_api_response_keys():
    r = client.get("/check_accessibility?lat=52.37&lon=4.89")
    assert r.status_code == 200

    data = r.json()
    assert "nearest_park" in data
    assert "distance_m" in data
    assert "accessible" in data
