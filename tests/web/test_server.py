from dataclasses import asdict
from fastapi.testclient import TestClient

from web.server import app
from core import api

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


def test_additional_action_endpoints() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    state = api.get_state()
    tiles = [asdict(t) for t in state.players[0].hand.tiles[:4]]

    resp = client.post(
        "/games/1/action",
        json={"player_index": 0, "action": "chi", "tiles": tiles[:3]},
    )
    assert resp.status_code == 200

    resp = client.post(
        "/games/1/action",
        json={"player_index": 0, "action": "pon", "tiles": tiles[:3]},
    )
    assert resp.status_code == 200

    resp = client.post(
        "/games/1/action",
        json={"player_index": 0, "action": "kan", "tiles": tiles},
    )
    assert resp.status_code == 200

    resp = client.post(
        "/games/1/action",
        json={"player_index": 0, "action": "riichi"},
    )
    assert resp.status_code == 200

    draw = client.post(
        "/games/1/action",
        json={"player_index": 0, "action": "draw"},
    )
    tile = draw.json()

    resp = client.post(
        "/games/1/action",
        json={"player_index": 0, "action": "tsumo", "tile": tile},
    )
    assert resp.status_code == 200

    resp = client.post(
        "/games/1/action",
        json={"player_index": 0, "action": "ron", "tile": tile},
    )
    assert resp.status_code == 200

    resp = client.post(
        "/games/1/action",
        json={"player_index": 0, "action": "skip"},
    )
    assert resp.status_code == 200


def test_draw_from_empty_wall_returns_error() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    from core import api
    assert api._engine is not None
    api._engine.state.wall.tiles = []  # type: ignore[list]
    resp = client.post(
        "/games/1/action",
        json={"player_index": 0, "action": "draw"},
    )
    assert resp.status_code == 409
    assert resp.json() == {"detail": "Wall is empty"}


def test_websocket_streams_events() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    with client.websocket_connect("/ws/1") as ws:
        data = ws.receive_json()
        assert data["name"] == "start_game"
        data = ws.receive_json()
        assert data["name"] == "start_kyoku"
        client.post(
            "/games/1/action",
            json={"player_index": 0, "action": "draw"},
        )
        data = ws.receive_json()
        assert data["name"] == "draw_tile"


def test_practice_endpoints() -> None:
    prob = client.get("/practice")
    assert prob.status_code == 200
    data = prob.json()
    assert "hand" in data and "dora_indicator" in data

    resp = client.post("/practice/suggest", json={"hand": data["hand"]})
    assert resp.status_code == 200
    tile = resp.json()
    assert "suit" in tile and "value" in tile
