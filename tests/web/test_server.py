from fastapi.testclient import TestClient

from web.server import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_get_game() -> None:
    create = client.post("/games", json={"players": ["A", "B", "C", "D"]})
    assert create.status_code == 200
    data = create.json()
    assert len(data["players"]) == 4

    response = client.get("/games/1")
    assert response.status_code == 200
    data = response.json()
    assert "players" in data
