from dataclasses import asdict
from fastapi.testclient import TestClient

from web.server import app
from core import api, models

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
    assert data["id"] == 1

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

    # Prepare chi on player 0 discard
    chi_tile = {"suit": "man", "value": 3}
    state.players[0].hand.tiles = [models.Tile(**chi_tile)]
    state.players[1].hand.tiles = []
    client.post(
        "/games/1/action",
        json={"player_index": 0, "action": "discard", "tile": chi_tile},
    )
    state.players[1].hand.tiles = [models.Tile("man", 1), models.Tile("man", 2)]
    resp = client.post(
        "/games/1/action",
        json={
            "player_index": 1,
            "action": "chi",
            "tiles": [
                {"suit": "man", "value": 1},
                {"suit": "man", "value": 2},
                chi_tile,
            ],
        },
    )
    assert resp.status_code == 200

    # Prepare pon on new discard
    pon_tile = {"suit": "pin", "value": 1}
    state.players[1].hand.tiles = [models.Tile(**pon_tile)]
    state.players[0].hand.tiles = []
    client.post(
        "/games/1/action",
        json={"player_index": 1, "action": "discard", "tile": pon_tile},
    )
    state.players[0].hand.tiles = [models.Tile("pin", 1), models.Tile("pin", 1)]
    resp = client.post(
        "/games/1/action",
        json={
            "player_index": 0,
            "action": "pon",
            "tiles": [
                pon_tile,
                {"suit": "pin", "value": 1},
                {"suit": "pin", "value": 1},
            ],
        },
    )
    assert resp.status_code == 200

    # Prepare kan on another discard
    kan_tile = {"suit": "sou", "value": 9}
    state.players[0].hand.tiles = [models.Tile(**kan_tile)]
    state.players[1].hand.tiles = []
    client.post(
        "/games/1/action",
        json={"player_index": 0, "action": "discard", "tile": kan_tile},
    )
    state.players[1].hand.tiles = [models.Tile("sou", 9) for _ in range(3)]
    resp = client.post(
        "/games/1/action",
        json={
            "player_index": 1,
            "action": "kan",
            "tiles": [
                kan_tile,
                {"suit": "sou", "value": 9},
                {"suit": "sou", "value": 9},
                {"suit": "sou", "value": 9},
            ],
        },
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
