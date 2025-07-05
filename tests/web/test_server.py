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


def test_draw_action_endpoint() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    resp = client.post(
        "/games/1/action",
        json={"player_index": 0, "action": "draw"},
    )
    assert resp.status_code == 200
    tile = resp.json()
    assert "suit" in tile and "value" in tile


def test_discard_action_endpoint() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    draw = client.post(
        "/games/1/action",
        json={"player_index": 0, "action": "draw"},
    )
    tile = draw.json()
    resp = client.post(
        "/games/1/action",
        json={"player_index": 0, "action": "discard", "tile": tile},
    )
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_websocket_streams_events() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    with client.websocket_connect("/ws/1") as ws:
        data = ws.receive_json()
        assert data["name"] == "start_game"
        client.post(
            "/games/1/action",
            json={"player_index": 0, "action": "draw"},
        )
        data = ws.receive_json()
        assert data["name"] == "draw_tile"
